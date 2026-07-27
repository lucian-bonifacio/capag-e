from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.assets.methodology import load_roa_methodology
from app.domain import (
    ComponentStatus,
    RoaAccountInput,
    RoaCashPressureInput,
    RoaRowStatus,
)
from app.domain.evidence import (
    EvidenceScopeType,
    EvidenceStatus,
    MethodComponent,
)
from app.engine import (
    build_adjustment_evidence,
    build_roa_audit_rows,
    build_roa_pressure_rows,
    calculate_roa,
)


METHODOLOGY = load_roa_methodology()
PRESSURE_TYPES = (
    "fornecedores_vencidos",
    "parcelamentos",
    "contingencias",
    "divida_fiscal",
    "divida_trabalhista",
    "mutuos",
    "intercompany",
)


def test_all_governed_pressures_reduce_final_roa_without_changing_preliminary() -> None:
    operating = build_roa_audit_rows(
        (_account("sales", "3.01.01.01.01.04", credit="1000"),),
        METHODOLOGY,
    )
    pressures = build_roa_pressure_rows(
        tuple(
            _pressure(pressure_type, str(index * 10))
            for index, pressure_type in enumerate(PRESSURE_TYPES, start=1)
        ),
        METHODOLOGY,
    )

    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=operating + pressures,
        methodology=METHODOLOGY,
        j150_available=False,
        materiality_base_value=Decimal("10000"),
    )

    assert calculation.roa_preliminary == Decimal("1000.00")
    assert calculation.cash_pressure_adjustments == Decimal("280.00")
    assert calculation.roa_final == Decimal("720.00")
    assert calculation.status == ComponentStatus.CALCULATED
    assert all(
        row.roa_block.value == "pressoes_complementares_caixa"
        for row in calculation.audit_rows[1:]
    )


def test_high_material_pressure_without_evidence_blocks_but_preserves_value() -> None:
    pressures = build_roa_pressure_rows(
        (_pressure("fornecedores_vencidos", "100"),),
        METHODOLOGY,
    )

    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=pressures,
        methodology=METHODOLOGY,
        j150_available=True,
        materiality_base_value=Decimal("1000"),
    )

    assert calculation.roa_final == Decimal("-100.00")
    assert calculation.status == ComponentStatus.BLOCKED_BY_EVIDENCE
    assert calculation.audit_rows[0].final_status == RoaRowStatus.PENDING_EVIDENCE
    assert calculation.pending_groups[0].code == "EVIDENCIA_ROA_MATERIAL_AUSENTE"


def test_validated_component_evidence_releases_material_pressure() -> None:
    pressures = build_roa_pressure_rows(
        (_pressure("fornecedores_vencidos", "100"),),
        METHODOLOGY,
    )

    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=pressures,
        methodology=METHODOLOGY,
        j150_available=True,
        materiality_base_value=Decimal("1000"),
        evidences=(
            _evidence(
                "fornecedores_vencidos",
                EvidenceScopeType.ROA_COMPONENT,
                EvidenceStatus.VALIDATED,
            ),
        ),
    )

    assert calculation.roa_final == Decimal("-100.00")
    assert calculation.status == ComponentStatus.CALCULATED
    assert calculation.audit_rows[0].evidence_id == "evidence-roa"


def test_rejected_expense_evidence_blocks_roa() -> None:
    expenses = build_roa_audit_rows(
        (_account("expense", "3.01.01.07.01.02", debit="100"),),
        METHODOLOGY,
    )

    calculation = calculate_roa(
        exercise_year=2024,
        audit_rows=expenses,
        methodology=METHODOLOGY,
        j150_available=True,
        materiality_base_value=Decimal("1000"),
        evidences=(
            _evidence(
                "expense",
                EvidenceScopeType.ACCOUNT,
                EvidenceStatus.REJECTED,
            ),
        ),
    )

    assert calculation.roa_final == Decimal("-100.00")
    assert calculation.status == ComponentStatus.BLOCKED_BY_EVIDENCE
    assert calculation.pending_groups[0].evidence_id == "evidence-roa"


def test_invalid_pressure_component_is_rejected() -> None:
    with pytest.raises(ValueError, match="cash pressure component"):
        build_roa_pressure_rows(
            (_pressure("receita_vendas_servicos", "10"),),
            METHODOLOGY,
        )


def _account(
    code: str,
    reference_code: str,
    *,
    debit: str = "0",
    credit: str = "0",
) -> RoaAccountInput:
    return RoaAccountInput(
        account_code=code,
        account_name=code,
        reference_code=reference_code,
        reference_description=reference_code,
        debit_amount=Decimal(debit),
        credit_amount=Decimal(credit),
        line_reference=1,
    )


def _pressure(pressure_type: str, amount: str) -> RoaCashPressureInput:
    return RoaCashPressureInput(
        pressure_id=f"pressure-{pressure_type}",
        pressure_type=pressure_type,
        account_code=f"account-{pressure_type}",
        account_name=pressure_type,
        reference_code=None,
        amount=Decimal(amount),
        source_reference="Cadastro controlado do analista.",
        line_reference=1,
    )


def _evidence(
    scope_key: str,
    scope_type: EvidenceScopeType,
    status: EvidenceStatus,
):
    return build_adjustment_evidence(
        evidence_id="evidence-roa",
        exercise_year=2024,
        scope_type=scope_type,
        scope_key=scope_key,
        adjustment_type="despesa_operacional_justificada",
        method_component=MethodComponent.ROA,
        amount_impact=Decimal("100"),
        impact_base_value=Decimal("1000"),
        required_evidence_type="documento_suporte",
        evidence_status=status,
        analyst_justification="Componente ROA conciliado.",
        review_notes=None,
        methodology_version_id="metodologia-2024.1",
        created_at=datetime(2026, 7, 24, tzinfo=timezone.utc),
    )

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.application import calculate_roa_plra_assessment
from app.domain import (
    CapagEMethod,
    CapagEStatus,
    ComponentStatus,
    DfcCalculation,
    PlraCalculation,
    RoaCalculation,
    RoaPendingGroup,
)


def test_calculated_roa_is_combined_with_external_plra() -> None:
    assessment = calculate_roa_plra_assessment(
        plra=_plra(),
        roa=_roa(),
    )

    assert assessment.method == CapagEMethod.ROA_PLRA
    assert assessment.plra_value == Decimal("500.00")
    assert assessment.roa_value == Decimal("80.00")
    assert assessment.capag_e_value == Decimal("580.00")
    assert assessment.capag_e_status == CapagEStatus.CALCULATED


def test_blocked_roa_blocks_assessment_and_preserves_values() -> None:
    assessment = calculate_roa_plra_assessment(
        plra=_plra(),
        roa=_roa(
            status=ComponentStatus.BLOCKED_BY_PENDING,
            pending_groups=(
                RoaPendingGroup(
                    code="CONTA_ROA_SEM_REGRA",
                    message="Conta sem regra.",
                    account_code="expense",
                    reference_code="3.99",
                    blocks_roa=True,
                ),
            ),
        ),
    )

    assert assessment.plra_value == Decimal("500.00")
    assert assessment.roa_value == Decimal("80.00")
    assert assessment.capag_e_value is None
    assert assessment.capag_e_status == CapagEStatus.BLOCKED
    assert "ROA_FINAL_INDISPONIVEL" in assessment.blocking_issues
    assert "ROA:CONTA_ROA_SEM_REGRA:expense" in assessment.blocking_issues


def test_blocked_plra_blocks_assessment_and_preserves_roa() -> None:
    assessment = calculate_roa_plra_assessment(
        plra=_plra(
            status=ComponentStatus.BLOCKED_BY_PENDING,
            blocking_issues=("ATIVO_PENDENTE",),
        ),
        roa=_roa(),
    )

    assert assessment.plra_value == Decimal("500.00")
    assert assessment.roa_value == Decimal("80.00")
    assert assessment.capag_e_value is None
    assert assessment.capag_e_status == CapagEStatus.BLOCKED
    assert "PLRA_FINAL_INDISPONIVEL" in assessment.blocking_issues
    assert "ATIVO_PENDENTE" in assessment.blocking_issues


def test_available_fca_preserves_both_comparison_paths() -> None:
    assessment = calculate_roa_plra_assessment(
        plra=_plra(),
        roa=_roa(),
        fca=_fca(),
    )

    assert assessment.method == CapagEMethod.COMPARATIVO_FCA_ROA
    assert assessment.capag_e_status == CapagEStatus.PARTIAL
    assert assessment.capag_e_value is None
    assert "PLRA+FCA=620.00" in assessment.calculation_basis
    assert "PLRA+ROA=580.00" in assessment.calculation_basis


def test_integration_rejects_different_methodology_versions() -> None:
    with pytest.raises(ValueError, match="same methodology version"):
        calculate_roa_plra_assessment(
            plra=_plra(),
            roa=_roa(methodology_version_id="other-version"),
        )


def _plra(
    *,
    status: ComponentStatus = ComponentStatus.CALCULATED,
    blocking_issues: tuple[str, ...] = (),
) -> PlraCalculation:
    return PlraCalculation(
        analysis_id="analysis-1",
        exercise_year=2024,
        gross_assets_value=Decimal("0"),
        gross_economic_liabilities_value=Decimal("0"),
        adjusted_assets_value=Decimal("0"),
        plr_gross_value=Decimal("0"),
        plra_value=Decimal("500"),
        plra_status=status,
        calculation_formula="snapshot externo",
        account_rows=(),
        pending_accounts=(),
        warnings=("PLRA preservado.",),
        limitations=(),
        blocking_issues=blocking_issues,
        j100_reconciliation_status="conciliado",
        methodology_version_id="metodologia-2024.1",
        calculated_at=datetime(2026, 7, 24, tzinfo=timezone.utc),
    )


def _roa(
    *,
    status: ComponentStatus = ComponentStatus.CALCULATED,
    pending_groups: tuple[RoaPendingGroup, ...] = (),
    methodology_version_id: str = "metodologia-2024.1",
) -> RoaCalculation:
    return RoaCalculation(
        exercise_year=2024,
        gross_revenue=Decimal("100"),
        deductions=Decimal("0"),
        revenue_taxes=Decimal("0"),
        net_operating_revenue=Decimal("100"),
        operating_costs=Decimal("10"),
        operating_expenses=Decimal("10"),
        financial_result=Decimal("0"),
        non_operating_result=Decimal("0"),
        cash_pressure_adjustments=Decimal("0"),
        roa_preliminary=Decimal("80"),
        roa_final=Decimal("80"),
        status=status,
        component_summaries=(),
        audit_rows=(),
        pending_groups=pending_groups,
        alerts=("ROA auditado.",),
        limitations=(),
        methodology_version_id=methodology_version_id,
    )


def _fca() -> DfcCalculation:
    return DfcCalculation(
        exercise_year=2024,
        automatic_value=Decimal("120"),
        operational_flow=Decimal("120"),
        investment_flow=Decimal("0"),
        financing_flow=Decimal("0"),
        manual_adjustments_value=Decimal("0"),
        fca_value=Decimal("120"),
        status=ComponentStatus.CALCULATED,
        component_summaries=(),
        audit_rows=(),
        pending_issues=(),
        alerts=(),
        limitations=(),
        methodology_version_id="metodologia-2024.1",
    )

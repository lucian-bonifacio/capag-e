from datetime import date, datetime, timezone
from decimal import Decimal

from app.assets.methodology import load_dfc_methodology
from app.domain.capag import ComponentStatus
from app.domain.dfc import (
    DfcEntry,
    DfcEntryItem,
    DfcManualAdjustment,
    DfcRowStatus,
)
from app.domain.evidence import (
    EvidenceScopeType,
    EvidenceStatus,
    MethodComponent,
)
from app.engine.dfc import build_dfc_audit_rows, calculate_dfc
from app.engine.evidence import build_adjustment_evidence


METHODOLOGY = load_dfc_methodology()


def test_calculates_fca_as_three_activities_plus_validated_adjustment() -> None:
    rows = _rows(
        _entry(
            "OP",
            _item("cash", "1.01.01.02.01", "100.00", "D", 2),
            _item("sales", "3.01.01.01.01.04", "100.00", "C", 3),
        ),
        _entry(
            "INV",
            _item("cash", "1.01.01.02.01", "200.00", "C", 4),
            _item("asset", "1.02.03.01.06", "200.00", "D", 5),
        ),
        _entry(
            "FIN",
            _item("cash", "1.01.01.02.01", "300.00", "D", 6),
            _item("loan", "2.02.01.01.06", "300.00", "C", 7),
        ),
    )
    calculation = calculate_dfc(
        exercise_year=2024,
        audit_rows=rows,
        methodology_version_id="metodologia-2024.1",
        materiality_base_value=Decimal("100000.00"),
        manual_adjustments=(
            DfcManualAdjustment(
                decision_id="decision-1",
                value=Decimal("25.00"),
                validated=True,
                justification="Ajuste conciliado.",
                evidence_id="evidence-1",
            ),
        ),
    )

    assert calculation.operational_flow == Decimal("100.00")
    assert calculation.investment_flow == Decimal("-200.00")
    assert calculation.financing_flow == Decimal("300.00")
    assert calculation.automatic_value == Decimal("200.00")
    assert calculation.manual_adjustments_value == Decimal("25.00")
    assert calculation.fca_value == Decimal("225.00")
    assert calculation.status == ComponentStatus.CALCULATED


def test_marks_operational_only_compatibility_input_as_partial_fca() -> None:
    calculation = calculate_dfc(
        exercise_year=2024,
        audit_rows=_rows(
            _entry(
                "FCO",
                _item("cash", "1.01.01.02.01", "100.00", "D", 2),
                _item("sales", "3.01.01.01.01.04", "100.00", "C", 3),
            )
        ),
        methodology_version_id="metodologia-2024.1",
        materiality_base_value=Decimal("100000.00"),
        complete_activity_scan=False,
    )

    assert calculation.fca_value == Decimal("100.00")
    assert calculation.status == ComponentStatus.PARTIAL
    assert "FCO" in calculation.limitations[0]


def test_material_unclassified_movement_blocks_final_fca() -> None:
    calculation = calculate_dfc(
        exercise_year=2024,
        audit_rows=_rows(
            _entry(
                "UNKNOWN",
                _item("cash", "1.01.01.02.01", "20.00", "D", 2),
                _item("other", "1.01.02.03.02", "20.00", "C", 3),
            )
        ),
        methodology_version_id="metodologia-2024.1",
        materiality_base_value=Decimal("1000.00"),
    )

    assert calculation.fca_value == Decimal("0.00")
    assert calculation.status == ComponentStatus.BLOCKED_BY_PENDING
    assert calculation.pending_issues[0].blocks_fca


def test_high_material_movement_without_evidence_blocks_but_preserves_value() -> None:
    calculation = calculate_dfc(
        exercise_year=2024,
        audit_rows=_rows(
            _entry(
                "MATERIAL",
                _item("cash", "1.01.01.02.01", "100.00", "D", 2),
                _item("sales", "3.01.01.01.01.04", "100.00", "C", 3),
            )
        ),
        methodology_version_id="metodologia-2024.1",
        materiality_base_value=Decimal("1000.00"),
    )

    assert calculation.fca_value == Decimal("100.00")
    assert calculation.status == ComponentStatus.BLOCKED_BY_EVIDENCE
    assert calculation.audit_rows[0].final_status == DfcRowStatus.PENDING_EVIDENCE


def test_validated_evidence_releases_material_movement_without_recalculation() -> None:
    rows = _rows(
        _entry(
            "MATERIAL",
            _item("cash", "1.01.01.02.01", "100.00", "D", 2),
            _item("sales", "3.01.01.01.01.04", "100.00", "C", 3),
        )
    )
    calculation = calculate_dfc(
        exercise_year=2024,
        audit_rows=rows,
        methodology_version_id="metodologia-2024.1",
        materiality_base_value=Decimal("1000.00"),
        evidences=(_evidence("MATERIAL:3", EvidenceStatus.VALIDATED),),
    )

    assert calculation.fca_value == Decimal("100.00")
    assert calculation.status == ComponentStatus.CALCULATED
    assert calculation.audit_rows[0].final_status == DfcRowStatus.INCLUDED


def test_pending_material_evidence_blocks_without_changing_calculated_value() -> None:
    rows = _rows(
        _entry(
            "MATERIAL",
            _item("cash", "1.01.01.02.01", "100.00", "D", 2),
            _item("sales", "3.01.01.01.01.04", "100.00", "C", 3),
        )
    )
    calculation = calculate_dfc(
        exercise_year=2024,
        audit_rows=rows,
        methodology_version_id="metodologia-2024.1",
        materiality_base_value=Decimal("1000.00"),
        evidences=(_evidence("MATERIAL:3", EvidenceStatus.PENDING),),
    )

    assert calculation.fca_value == Decimal("100.00")
    assert calculation.status == ComponentStatus.BLOCKED_BY_EVIDENCE


def test_unvalidated_manual_adjustment_is_excluded_and_blocks() -> None:
    calculation = calculate_dfc(
        exercise_year=2024,
        audit_rows=_rows(
            _entry(
                "OP",
                _item("cash", "1.01.01.02.01", "100.00", "D", 2),
                _item("sales", "3.01.01.01.01.04", "100.00", "C", 3),
            )
        ),
        methodology_version_id="metodologia-2024.1",
        materiality_base_value=Decimal("100000.00"),
        manual_adjustments=(
            DfcManualAdjustment(
                decision_id="decision-1",
                value=Decimal("50.00"),
                validated=False,
                justification="Aguardando validacao.",
                evidence_id=None,
            ),
        ),
    )

    assert calculation.manual_adjustments_value == Decimal("0.00")
    assert calculation.fca_value == Decimal("100.00")
    assert calculation.status == ComponentStatus.BLOCKED_BY_PENDING


def _evidence(scope_key: str, status: EvidenceStatus):
    return build_adjustment_evidence(
        evidence_id=f"evidence-{status.value}",
        exercise_year=2024,
        scope_type=EvidenceScopeType.FCO_MOVEMENT,
        scope_key=scope_key,
        adjustment_type="fluxo_incluido",
        method_component=MethodComponent.FCA,
        amount_impact=Decimal("100.00"),
        impact_base_value=Decimal("1000.00"),
        required_evidence_type="extrato_bancario",
        evidence_status=status,
        analyst_justification="Movimento conciliado.",
        review_notes=None,
        methodology_version_id="metodologia-2024.1",
        created_at=datetime(2024, 1, 31, tzinfo=timezone.utc),
    )


def _rows(*entries: DfcEntry):
    return build_dfc_audit_rows(tuple(entries), METHODOLOGY, year=2024)


def _entry(number: str, *items: DfcEntryItem) -> DfcEntry:
    return DfcEntry(
        entry_number=number,
        entry_date=date(2024, 1, 31),
        items=tuple(items),
    )


def _item(
    code: str,
    reference: str | None,
    amount: str,
    indicator: str,
    line: int,
) -> DfcEntryItem:
    return DfcEntryItem(
        account_code=code,
        account_name=code,
        reference_code=reference,
        amount=Decimal(amount),
        debit_credit_indicator=indicator,
        history="Historico",
        line_number=line,
    )

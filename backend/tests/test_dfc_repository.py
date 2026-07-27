from datetime import date, datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.assets.methodology import load_dfc_methodology
from app.domain import (
    DfcDecisionAction,
    DfcEntry,
    DfcEntryItem,
    DfcManualDecision,
)
from app.engine import build_dfc_audit_rows, calculate_dfc
from app.repositories import (
    Base,
    DfcAuditRowModel,
    DfcCalculationModel,
    DfcCalculationNotFound,
    add_dfc_calculation,
    get_latest_dfc_calculation,
    invalidate_dfc_calculations,
    list_dfc_manual_decisions,
    save_dfc_manual_decision,
)


def test_dfc_repository_preserves_snapshot_audit_and_decision() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    calculation = _calculation()
    decision = DfcManualDecision(
        decision_id="decision-1",
        entry_number="LCTO-1",
        line_number=3,
        action=DfcDecisionAction.EXCLUDE,
        activity=None,
        component_code=None,
        justification="Movimento duplicado confirmado.",
        evidence_id=None,
        decided_at=datetime(2024, 12, 31, tzinfo=timezone.utc),
        methodology_version_id="metodologia-2024.1",
    )

    with Session(engine) as session:
        add_dfc_calculation(
            session,
            exercise_id=7,
            analysis_id="analysis-1",
            calculation=calculation,
        )
        save_dfc_manual_decision(session, exercise_id=7, decision=decision)
        session.commit()

        stored = session.scalar(select(DfcCalculationModel))
        audit = session.scalar(select(DfcAuditRowModel))
        restored = get_latest_dfc_calculation(session, exercise_id=7)
        decisions = list_dfc_manual_decisions(session, exercise_id=7)

    assert stored is not None
    assert stored.snapshot_json["fca_value"] == "100.00"
    assert audit is not None
    assert audit.snapshot_json["entry_number"] == "LCTO-1"
    assert restored.fca_value == Decimal("100.00")
    assert restored.audit_rows[0].counterparty_account_name == "Venda"
    assert decisions == [decision]


def test_invalidated_dfc_snapshot_is_not_returned() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        add_dfc_calculation(
            session,
            exercise_id=7,
            analysis_id="analysis-1",
            calculation=_calculation(),
        )
        session.commit()
        assert invalidate_dfc_calculations(session, exercise_id=7) == 1
        session.commit()

        with pytest.raises(DfcCalculationNotFound):
            get_latest_dfc_calculation(session, exercise_id=7)


def _calculation():
    methodology = load_dfc_methodology()
    rows = build_dfc_audit_rows(
        (
            DfcEntry(
                entry_number="LCTO-1",
                entry_date=date(2024, 1, 31),
                items=(
                    DfcEntryItem(
                        account_code="cash",
                        account_name="Banco",
                        reference_code="1.01.01.02.01",
                        amount=Decimal("100.00"),
                        debit_credit_indicator="D",
                        history="Recebimento",
                        line_number=2,
                    ),
                    DfcEntryItem(
                        account_code="sales",
                        account_name="Venda",
                        reference_code="3.01.01.01.01.04",
                        amount=Decimal("100.00"),
                        debit_credit_indicator="C",
                        history="Recebimento",
                        line_number=3,
                    ),
                ),
            ),
        ),
        methodology,
        year=2024,
    )
    return calculate_dfc(
        exercise_year=2024,
        audit_rows=rows,
        methodology_version_id="metodologia-2024.1",
        materiality_base_value=Decimal("100000.00"),
    )

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.domain import ComponentStatus, PlraAccountInput
from app.engine import calculate_capag_e_assessment, calculate_plra
from app.assets.methodology import load_plra_policy
from app.repositories import (
    Base,
    CapagAssessmentNotFound,
    PlraAuditRowModel,
    PlraCalculationModel,
    add_capag_assessment,
    add_plra_calculation,
    get_latest_capag_assessment,
    get_latest_plra_calculation,
    invalidate_capag_assessments,
)


def test_plra_repository_preserves_runs_and_audit_rows() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    first = _calculation("100")
    second = _calculation("200")

    with Session(engine) as session:
        add_plra_calculation(session, exercise_id=7, calculation=first)
        add_plra_calculation(session, exercise_id=7, calculation=second)
        session.commit()

        stored = session.scalars(
            select(PlraCalculationModel).order_by(PlraCalculationModel.id)
        ).all()
        rows = session.scalars(select(PlraAuditRowModel)).all()
        latest = get_latest_plra_calculation(session, exercise_id=7)

    assert len(stored) == 2
    assert len(rows) == 2
    assert stored[0].snapshot_json["plra_value"] == "100.00"
    assert latest.plra_value == Decimal("200.00")
    assert latest.account_rows[0].methodology_group == "caixa"


def test_invalidated_capag_assessment_is_not_returned() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    assessment = calculate_capag_e_assessment(
        exercise_year=2024,
        method="fca_plra",
        plra_value=Decimal("100"),
        plra_status=ComponentStatus.CALCULATED,
        fco_value=Decimal("20"),
        methodology_version_id="metodologia-2024.1",
    )

    with Session(engine) as session:
        add_capag_assessment(session, exercise_id=7, assessment=assessment)
        session.commit()
        assert invalidate_capag_assessments(session, exercise_id=7) == 1
        session.commit()

        with pytest.raises(CapagAssessmentNotFound):
            get_latest_capag_assessment(session, exercise_id=7)


def _calculation(value: str):
    return calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[
            PlraAccountInput(
                account_code="cash",
                account_name="Caixa",
                account_type="A",
                account_level=5,
                parent_account_code=None,
                declared_reference_code="1.01.01.01.01",
                official_description="Caixa Matriz",
                official_nature="ATIVO",
                final_balance=Decimal(value),
                final_balance_indicator="D",
            )
        ],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        j100_available=True,
        calculated_at=datetime(2024, 12, 31, tzinfo=timezone.utc),
    )


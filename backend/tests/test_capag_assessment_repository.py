from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.domain import CapagEMethod, ComponentStatus
from app.engine import calculate_capag_e_assessment
from app.repositories import (
    Base,
    CapagAssessmentModel,
    add_capag_assessment,
    get_latest_capag_assessment,
)


def test_capag_assessment_snapshot_preserves_statuses_and_messages() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    assessment = calculate_capag_e_assessment(
        exercise_year=2024,
        method=CapagEMethod.FCA_PLRA,
        plra_value=Decimal("500000.00"),
        plra_status=ComponentStatus.CALCULATED,
        fco_value=Decimal("40000.00"),
        warnings=("Valor sujeito a revisao.",),
        blocking_issues=("EVIDENCIA_PENDENTE",),
        methodology_version_id="metodologia-2024.1",
    )

    with Session(engine) as session:
        add_capag_assessment(session, exercise_id=7, assessment=assessment)
        session.commit()

        stored = session.scalar(select(CapagAssessmentModel))
        restored = get_latest_capag_assessment(session, exercise_id=7)

    assert stored is not None
    assert stored.method == "fca_plra"
    assert stored.fca_status == "parcial"
    assert stored.capag_e_status == "parcial"
    assert stored.snapshot_json["fca_value"] == "40000.00"
    assert restored.method == CapagEMethod.FCA_PLRA
    assert restored.fca_status == ComponentStatus.PARTIAL
    assert restored.limitations == (
        "FCA parcial: somente o fluxo de caixa operacional (FCO) esta disponivel.",
        "Resultado parcial: FCA ainda nao possui status calculado.",
    )
    assert restored.blocking_issues == ("EVIDENCIA_PENDENTE",)

from decimal import Decimal
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.application import (
    EcdImportIdentifiers,
    get_plra_calculation,
    persist_parsed_ecd,
    run_plra_calculation,
)
from app.assets.methodology import EXPECTED_DEFAULT_DISCOUNTS, PlraPolicy, PlraRule
from app.domain import ComponentStatus
from app.engine import calculate_capag_e_assessment
from app.engine.methodology_matcher import OfficialReferenceAccount
from app.io import parse_ecd_file
from app.repositories import (
    Base,
    CapagAssessmentModel,
    ExerciseModel,
    PlraCalculationModel,
    EcdFileModel,
    add_capag_assessment,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "ecd"


def test_plra_service_persists_new_snapshots_and_invalidates_capag() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    parsed = parse_ecd_file(FIXTURES_DIR / "valid_declared.ecd")

    with Session(engine) as session:
        persisted = persist_parsed_ecd(
            session,
            parsed_ecd=parsed,
            identifiers=EcdImportIdentifiers(
                company_id="company",
                ecd_file_id="ecd",
                analysis_id="analysis",
                methodology_version_id="metodologia-2024.1",
                original_filename="valid_declared.ecd",
                content_hash="fixture-plra",
            ),
        )
        exercise = session.scalar(
            select(ExerciseModel).where(
                ExerciseModel.analysis_id == persisted.analysis_id
            )
        )
        assert exercise is not None
        ecd_file = session.get(EcdFileModel, "ecd")
        assert ecd_file is not None
        ecd_file.layout = "LECD"
        add_capag_assessment(
            session,
            exercise_id=exercise.id,
            assessment=calculate_capag_e_assessment(
                exercise_year=2024,
                method="fca_plra",
                plra_value=Decimal("1"),
                plra_status=ComponentStatus.CALCULATED,
                fco_value=Decimal("1"),
                methodology_version_id="metodologia-2024.1",
            ),
        )
        session.commit()

        first = run_plra_calculation(
            session,
            analysis_id="analysis",
            year=2024,
            policy=_fixture_policy(),
            official_references=[_fixture_official_reference()],
        )
        second = run_plra_calculation(
            session,
            analysis_id="analysis",
            year=2024,
            policy=_fixture_policy(),
            official_references=[_fixture_official_reference()],
        )

        stored_runs = session.scalars(select(PlraCalculationModel)).all()
        capag = session.scalar(select(CapagAssessmentModel))
        latest = get_plra_calculation(session, analysis_id="analysis", year=2024)

    assert first.plra_value == Decimal("-100000.00")
    assert second.plra_value == Decimal("-100000.00")
    assert len(stored_runs) == 2
    assert capag is not None and capag.invalidated_at is not None
    assert latest.plra_value == second.plra_value


def _fixture_policy() -> PlraPolicy:
    return PlraPolicy(
        methodology_version_id="metodologia-2024.1",
        status="ATIVA",
        source="fixture",
        default_discounts=EXPECTED_DEFAULT_DISCOUNTS,
        rules=(
            PlraRule(
                methodology_rule_id="fixture-liability",
                reference_code="2.01.01.07.01",
                methodology_group="emprestimos_financiamentos",
                macrogroup="PASSIVO_EXIGIVEL",
                treatment="INCLUIR_PASSIVO",
                default_discount_group=None,
                rule_status="ATIVA",
                valid_from=2024,
                valid_to=None,
                reason="Passivo de fixture.",
            ),
        ),
    )


def _fixture_official_reference() -> OfficialReferenceAccount:
    return OfficialReferenceAccount(
        reference_code="2.01.01.07.01",
        official_description="Emprestimos e financiamentos",
        parent_reference_code=None,
        level=5,
        nature="PASSIVO",
        valid_from=2024,
        valid_to=None,
        layout="ECD_9",
        entity_type="PJ_GERAL",
        source="fixture",
        status="ATIVA",
        methodology_version_id="metodologia-2024.1",
    )

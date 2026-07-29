from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.assets.methodology import load_plra_policy
from app.domain import (
    AssetRealizability,
    ComponentStatus,
    EssentialityStatus,
    EvidenceScopeType,
    EvidenceStatus,
    MaterialityLevel,
    MethodComponent,
    PlraAccountInput,
    ValuationBasis,
    ValuationStatus,
)
from app.engine import (
    apply_materiality_override,
    assess_asset_valuation,
    build_adjustment_evidence,
    calculate_plra,
)
from app.repositories import (
    AdjustmentEvidenceModel,
    AssetValuationAssessmentModel,
    Base,
    PlraCalculationNotFound,
    add_plra_calculation,
    get_adjustment_evidence,
    get_asset_valuation,
    get_latest_plra_calculation,
    invalidate_plra_calculations,
    list_adjustment_evidences,
    list_asset_valuations,
    save_adjustment_evidence,
    save_asset_valuation,
)


def test_evidence_and_asset_valuation_round_trip() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    evidence = _evidence()
    valuation = _valuation(evidence=evidence)

    with Session(engine) as session:
        save_adjustment_evidence(
            session, exercise_id=7, evidence=evidence
        )
        save_asset_valuation(
            session, exercise_id=7, assessment=valuation
        )
        session.commit()

        stored_evidence = get_adjustment_evidence(
            session, evidence_id=evidence.evidence_id
        )
        stored_valuation = get_asset_valuation(
            session, assessment_id=valuation.assessment_id
        )

    assert stored_evidence.to_snapshot() == evidence.to_snapshot()
    assert stored_valuation.to_snapshot() == valuation.to_snapshot()
    assert stored_valuation.evidence_id == evidence.evidence_id


def test_evidence_update_preserves_override_history_without_duplicate_row() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    evidence = _evidence()
    overridden = apply_materiality_override(
        evidence,
        materiality_level=MaterialityLevel.HIGH,
        justification="Impact operacional confirmado.",
        overridden_at=datetime(2026, 7, 24, 21, tzinfo=timezone.utc),
    )

    with Session(engine) as session:
        save_adjustment_evidence(session, exercise_id=7, evidence=evidence)
        save_adjustment_evidence(
            session, exercise_id=7, evidence=overridden
        )
        session.commit()

        rows = session.scalars(select(AdjustmentEvidenceModel)).all()
        listed = list_adjustment_evidences(
            session,
            exercise_id=7,
            method_component=MethodComponent.PLRA,
        )

    assert len(rows) == 1
    assert listed[0].materiality_level == MaterialityLevel.HIGH
    assert len(listed[0].materiality_overrides) == 1


def test_asset_valuation_list_is_scoped_by_exercise() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    evidence = _evidence()
    valuation = _valuation(evidence=evidence)

    with Session(engine) as session:
        save_adjustment_evidence(session, exercise_id=7, evidence=evidence)
        save_asset_valuation(session, exercise_id=7, assessment=valuation)
        session.commit()

        assert len(list_asset_valuations(session, exercise_id=7)) == 1
        assert list_asset_valuations(session, exercise_id=8) == []
        assert len(
            session.scalars(select(AssetValuationAssessmentModel)).all()
        ) == 1


def test_evidence_change_can_invalidate_plra_snapshot() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    calculation = _plra()

    with Session(engine) as session:
        add_plra_calculation(
            session, exercise_id=7, calculation=calculation
        )
        session.commit()
        assert invalidate_plra_calculations(session, exercise_id=7) == 1
        session.commit()

        with pytest.raises(PlraCalculationNotFound):
            get_latest_plra_calculation(session, exercise_id=7)


def test_plra_uses_persistable_asset_value_and_propagates_evidence_block() -> None:
    evidence = _evidence(
        amount_impact=Decimal("100.00"),
        evidence_status=EvidenceStatus.PENDING,
    )
    valuation = _valuation(
        evidence=None,
        valuation_required=True,
        valuation_status=ValuationStatus.PENDING,
        forced_liquidation_value=Decimal("450.00"),
        valuation_basis=ValuationBasis.ABNT_NBR_14653_REPORT,
    )

    calculation = _plra(
        evidences=[evidence],
        asset_valuations=[valuation],
    )

    assert calculation.plra_value == Decimal("200.00")
    assert calculation.plra_status == ComponentStatus.BLOCKED_BY_EVIDENCE
    assert any(
        issue.startswith("EVIDENCIA_BLOQUEANTE")
        for issue in calculation.blocking_issues
    )


def test_plra_uses_validated_asset_value() -> None:
    evidence = _evidence()
    valuation = _valuation(
        evidence=evidence,
        valuation_required=True,
        valuation_status=ValuationStatus.VALIDATED,
        forced_liquidation_value=Decimal("450.00"),
        valuation_basis=ValuationBasis.ABNT_NBR_14653_REPORT,
    )

    calculation = _plra(
        evidences=[evidence],
        asset_valuations=[valuation],
    )

    assert calculation.plra_value == Decimal("450.00")
    assert calculation.plra_status == ComponentStatus.CALCULATED
    assert (
        calculation.account_rows[0].valuation_source
        == "liquidacao_forcada_validada"
    )


def _evidence(
    *,
    amount_impact: Decimal = Decimal("20.00"),
    evidence_status: EvidenceStatus = EvidenceStatus.VALIDATED,
):
    return build_adjustment_evidence(
        evidence_id="evidence-asset-1",
        exercise_year=2024,
        scope_type=EvidenceScopeType.ACCOUNT,
        scope_key="asset-1",
        adjustment_type="avaliacao_ativo",
        method_component=MethodComponent.PLRA,
        amount_impact=amount_impact,
        impact_base_value=Decimal("1000.00"),
        required_evidence_type="laudo_abnt_nbr_14653",
        evidence_status=evidence_status,
        analyst_justification="Ativo avaliado com suporte documental.",
        review_notes=None,
        methodology_version_id="metodologia-2024.1",
        created_at=datetime(2026, 7, 24, tzinfo=timezone.utc),
    )


def _valuation(
    *,
    evidence,
    valuation_required: bool = True,
    valuation_status: ValuationStatus = ValuationStatus.VALIDATED,
    forced_liquidation_value: Decimal | None = Decimal("450.00"),
    valuation_basis: ValuationBasis = ValuationBasis.ABNT_NBR_14653_REPORT,
):
    return assess_asset_valuation(
        assessment_id="valuation-asset-1",
        exercise_year=2024,
        account_code="asset-1",
        account_name="Maquinas e equipamentos",
        reference_code="1.02.03.01.06",
        book_value=Decimal("1000.00"),
        policy=load_plra_policy(),
        realizability_classification=(
            AssetRealizability.FORCED_LIQUIDATION_REQUIRES_REPORT
        ),
        valuation_required=valuation_required,
        valuation_basis=valuation_basis,
        forced_liquidation_value=forced_liquidation_value,
        analyst_adjusted_value=None,
        essentiality_status=EssentialityStatus.NOT_ESSENTIAL,
        valuation_status=valuation_status,
        evidence=evidence,
    )


def _plra(*, evidences=None, asset_valuations=None):
    return calculate_plra(
        analysis_id="analysis",
        exercise_year=2024,
        accounts=[
            PlraAccountInput(
                account_code="asset-1",
                account_name="Maquinas e equipamentos",
                account_type="A",
                account_level=5,
                parent_account_code=None,
                declared_reference_code="1.02.03.01.06",
                official_description="Maquinas e Equipamentos",
                official_nature="ATIVO",
                final_balance=Decimal("1000.00"),
                final_balance_indicator="D",
            )
        ],
        policy=load_plra_policy(),
        methodology_version_id="metodologia-2024.1",
        evidences=evidences,
        asset_valuations=asset_valuations,
        balance_status="VALIDO",
        calculated_at=datetime(2026, 7, 24, tzinfo=timezone.utc),
    )

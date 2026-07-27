from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.assets.methodology import load_plra_policy
from app.domain import (
    AdjustmentEvidence,
    AssetRealizability,
    AssetValuationAssessment,
    EssentialityStatus,
    EvidenceScopeType,
    EvidenceStatus,
    MaterialityLevel,
    MethodComponent,
    ValuationBasis,
    ValuationStatus,
)
from app.engine import (
    apply_materiality_override,
    assess_asset_valuation,
    build_adjustment_evidence,
    revise_adjustment_evidence,
)
from app.repositories import (
    AdjustmentEvidenceModel,
    AnalysisModel,
    AssetValuationAssessmentModel,
    EcdI050AccountModel,
    EcdI051ReferenceLinkModel,
    EcdI155BalanceModel,
    EvidenceNotFound,
    ExerciseModel,
    get_adjustment_evidence,
    invalidate_capag_assessments,
    invalidate_dfc_calculations,
    invalidate_plra_calculations,
    list_adjustment_evidences,
    list_asset_valuations,
    save_adjustment_evidence,
    save_asset_valuation,
)


class EvidenceContextNotFound(LookupError):
    pass


class EvidenceOperationUnavailable(RuntimeError):
    pass


def create_evidence(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    scope_type: EvidenceScopeType,
    scope_key: str,
    adjustment_type: str,
    method_component: MethodComponent,
    amount_impact: Decimal,
    impact_base_value: Decimal | None,
    required_evidence_type: str | None,
    evidence_status: EvidenceStatus,
    analyst_justification: str | None,
    review_notes: str | None,
    can_change_capag_status: bool,
    can_reverse_prudential_sign: bool,
) -> AdjustmentEvidence:
    try:
        analysis, exercise = _get_context(
            session, analysis_id=analysis_id, year=year
        )
        evidence = build_adjustment_evidence(
            evidence_id=f"evidence-{uuid4().hex}",
            exercise_year=year,
            scope_type=scope_type,
            scope_key=scope_key,
            adjustment_type=adjustment_type,
            method_component=method_component,
            amount_impact=amount_impact,
            impact_base_value=impact_base_value,
            required_evidence_type=required_evidence_type,
            evidence_status=evidence_status,
            analyst_justification=analyst_justification,
            review_notes=review_notes,
            methodology_version_id=(
                exercise.methodology_version_id
                or analysis.methodology_version_id
            ),
            can_change_capag_status=can_change_capag_status,
            can_reverse_prudential_sign=can_reverse_prudential_sign,
        )
        save_adjustment_evidence(
            session, exercise_id=exercise.id, evidence=evidence
        )
        _invalidate_dependents(session, exercise_id=exercise.id)
        session.commit()
        return evidence
    except (EvidenceContextNotFound, TypeError, ValueError):
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise EvidenceOperationUnavailable(
            "Evidence creation failed."
        ) from exc


def revise_evidence(
    session: Session,
    *,
    evidence_id: str,
    required_evidence_type: str | None,
    evidence_status: EvidenceStatus,
    analyst_justification: str | None,
    review_notes: str | None,
    override_level: MaterialityLevel | None,
    override_justification: str | None,
) -> AdjustmentEvidence:
    try:
        model = session.scalar(
            select(AdjustmentEvidenceModel).where(
                AdjustmentEvidenceModel.evidence_id == evidence_id
            )
        )
        if model is None:
            raise EvidenceContextNotFound("Adjustment evidence not found.")
        evidence = revise_adjustment_evidence(
            model.to_domain(),
            evidence_status=evidence_status,
            required_evidence_type=required_evidence_type,
            analyst_justification=analyst_justification,
            review_notes=review_notes,
        )
        if override_level is not None:
            evidence = apply_materiality_override(
                evidence,
                materiality_level=override_level,
                justification=override_justification or "",
            )
        save_adjustment_evidence(
            session,
            exercise_id=model.exercise_id,
            evidence=evidence,
        )
        _invalidate_dependents(session, exercise_id=model.exercise_id)
        session.commit()
        return evidence
    except (EvidenceContextNotFound, TypeError, ValueError):
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise EvidenceOperationUnavailable(
            "Evidence revision failed."
        ) from exc


def get_evidences(
    session: Session,
    *,
    analysis_id: str,
    year: int,
    method_component: MethodComponent | None = None,
    evidence_status: EvidenceStatus | None = None,
) -> list[AdjustmentEvidence]:
    try:
        _, exercise = _get_context(
            session, analysis_id=analysis_id, year=year
        )
        evidences = list_adjustment_evidences(
            session,
            exercise_id=exercise.id,
            method_component=method_component,
        )
        if evidence_status is not None:
            evidences = [
                evidence
                for evidence in evidences
                if evidence.evidence_status == evidence_status
            ]
        return evidences
    except SQLAlchemyError as exc:
        raise EvidenceOperationUnavailable(
            "Evidence query failed."
        ) from exc


def get_asset_valuations(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> list[AssetValuationAssessment]:
    try:
        _, exercise = _get_context(
            session, analysis_id=analysis_id, year=year
        )
        return list_asset_valuations(session, exercise_id=exercise.id)
    except SQLAlchemyError as exc:
        raise EvidenceOperationUnavailable(
            "Asset valuation query failed."
        ) from exc


def update_asset_valuation(
    session: Session,
    *,
    assessment_id: str,
    analysis_id: str,
    year: int,
    account_code: str,
    realizability_classification: AssetRealizability,
    valuation_required: bool,
    valuation_basis: ValuationBasis,
    forced_liquidation_value: Decimal | None,
    analyst_adjusted_value: Decimal | None,
    essentiality_status: EssentialityStatus,
    valuation_status: ValuationStatus,
    evidence_id: str | None,
) -> AssetValuationAssessment:
    try:
        analysis, exercise = _get_context(
            session, analysis_id=analysis_id, year=year
        )
        existing = session.scalar(
            select(AssetValuationAssessmentModel).where(
                AssetValuationAssessmentModel.assessment_id == assessment_id
            )
        )
        if existing is not None and existing.exercise_id != exercise.id:
            raise ValueError("Asset valuation belongs to another exercise.")

        account_name, reference_code, book_value = _asset_account_context(
            session,
            exercise_id=exercise.id,
            account_code=account_code,
        )
        evidence = None
        if evidence_id is not None:
            evidence_model = session.scalar(
                select(AdjustmentEvidenceModel).where(
                    AdjustmentEvidenceModel.evidence_id == evidence_id
                )
            )
            if evidence_model is None:
                raise EvidenceContextNotFound(
                    "Adjustment evidence not found."
                )
            if evidence_model.exercise_id != exercise.id:
                raise ValueError("Evidence belongs to another exercise.")
            evidence = get_adjustment_evidence(
                session, evidence_id=evidence_id
            )

        methodology_version_id = (
            exercise.methodology_version_id
            or analysis.methodology_version_id
        )
        policy = load_plra_policy()
        if policy.methodology_version_id != methodology_version_id:
            raise ValueError(
                "PLRA policy and analysis methodology versions differ."
            )
        assessment = assess_asset_valuation(
            assessment_id=assessment_id,
            exercise_year=year,
            account_code=account_code,
            account_name=account_name,
            reference_code=reference_code,
            book_value=book_value,
            policy=policy,
            realizability_classification=realizability_classification,
            valuation_required=valuation_required,
            valuation_basis=valuation_basis,
            forced_liquidation_value=forced_liquidation_value,
            analyst_adjusted_value=analyst_adjusted_value,
            essentiality_status=essentiality_status,
            valuation_status=valuation_status,
            evidence=evidence,
        )
        save_asset_valuation(
            session,
            exercise_id=exercise.id,
            assessment=assessment,
        )
        _invalidate_dependents(session, exercise_id=exercise.id)
        session.commit()
        return assessment
    except (EvidenceContextNotFound, TypeError, ValueError):
        session.rollback()
        raise
    except SQLAlchemyError as exc:
        session.rollback()
        raise EvidenceOperationUnavailable(
            "Asset valuation update failed."
        ) from exc


def _get_context(
    session: Session, *, analysis_id: str, year: int
) -> tuple[AnalysisModel, ExerciseModel]:
    analysis = session.get(AnalysisModel, analysis_id)
    if analysis is None:
        raise EvidenceContextNotFound("Analysis not found.")
    exercise = session.scalar(
        select(ExerciseModel)
        .where(ExerciseModel.analysis_id == analysis_id)
        .where(ExerciseModel.year == year)
    )
    if exercise is None:
        raise EvidenceContextNotFound("Exercise not found.")
    return analysis, exercise


def _asset_account_context(
    session: Session,
    *,
    exercise_id: int,
    account_code: str,
) -> tuple[str, str, Decimal]:
    account = session.scalar(
        select(EcdI050AccountModel)
        .where(EcdI050AccountModel.exercise_id == exercise_id)
        .where(EcdI050AccountModel.account_code == account_code)
    )
    if account is None:
        raise EvidenceContextNotFound("ECD account not found.")
    links = list(
        session.scalars(
            select(EcdI051ReferenceLinkModel)
            .where(EcdI051ReferenceLinkModel.exercise_id == exercise_id)
            .where(EcdI051ReferenceLinkModel.account_code == account_code)
        )
    )
    reference_codes = {link.reference_code for link in links}
    if len(reference_codes) != 1:
        raise ValueError(
            "Asset valuation requires one exact declared reference code."
        )
    balance = session.scalar(
        select(EcdI155BalanceModel)
        .where(EcdI155BalanceModel.exercise_id == exercise_id)
        .where(EcdI155BalanceModel.account_code == account_code)
        .order_by(EcdI155BalanceModel.line_number.desc())
        .limit(1)
    )
    if balance is None:
        raise EvidenceContextNotFound("ECD account balance not found.")
    multiplier = (
        Decimal("1")
        if balance.final_balance_indicator == "D"
        else Decimal("-1")
    )
    return (
        account.account_name,
        next(iter(reference_codes)),
        balance.final_balance * multiplier,
    )


def _invalidate_dependents(session: Session, *, exercise_id: int) -> None:
    invalidate_plra_calculations(session, exercise_id=exercise_id)
    invalidate_dfc_calculations(session, exercise_id=exercise_id)
    invalidate_capag_assessments(session, exercise_id=exercise_id)

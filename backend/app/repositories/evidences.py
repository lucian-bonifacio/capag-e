from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    select,
)
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.domain import (
    AdjustmentEvidence,
    AssetRealizability,
    AssetValuationAssessment,
    EssentialityStatus,
    EvidenceScopeType,
    EvidenceStatus,
    MaterialityLevel,
    MaterialityOverride,
    MaterialitySource,
    MethodComponent,
    ValuationBasis,
    ValuationStatus,
    ValuationValueSource,
)
from app.repositories.declared_snapshots import Base


class AdjustmentEvidenceModel(Base):
    __tablename__ = "adjustment_evidences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    evidence_id: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"), nullable=False, index=True
    )
    exercise_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    scope_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    scope_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    adjustment_type: Mapped[str] = mapped_column(String(80), nullable=False)
    method_component: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )
    amount_impact: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    impact_base_value: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2), nullable=True
    )
    impact_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 6), nullable=True
    )
    materiality_level: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )
    materiality_source: Mapped[str] = mapped_column(String(30), nullable=False)
    minimum_materiality_level: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    required_evidence_type: Mapped[str | None] = mapped_column(
        String(120), nullable=True
    )
    evidence_status: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    analyst_justification: Mapped[str | None] = mapped_column(Text(), nullable=True)
    review_notes: Mapped[str | None] = mapped_column(Text(), nullable=True)
    blocks_final_report: Mapped[bool] = mapped_column(
        Boolean, nullable=False, index=True
    )
    requires_reservation: Mapped[bool] = mapped_column(Boolean, nullable=False)
    human_review_required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    decision_reasons_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    materiality_overrides_json: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, nullable=False
    )
    methodology_version_id: Mapped[str] = mapped_column(
        String(120), nullable=False, index=True
    )
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    def to_domain(self) -> AdjustmentEvidence:
        return AdjustmentEvidence(
            evidence_id=self.evidence_id,
            exercise_year=self.exercise_year,
            scope_type=EvidenceScopeType(self.scope_type),
            scope_key=self.scope_key,
            adjustment_type=self.adjustment_type,
            method_component=MethodComponent(self.method_component),
            amount_impact=self.amount_impact,
            impact_base_value=self.impact_base_value,
            impact_percent=self.impact_percent,
            materiality_level=MaterialityLevel(self.materiality_level),
            materiality_source=MaterialitySource(self.materiality_source),
            minimum_materiality_level=MaterialityLevel(
                self.minimum_materiality_level
            ),
            required_evidence_type=self.required_evidence_type,
            evidence_status=EvidenceStatus(self.evidence_status),
            analyst_justification=self.analyst_justification,
            review_notes=self.review_notes,
            blocks_final_report=self.blocks_final_report,
            requires_reservation=self.requires_reservation,
            human_review_required=self.human_review_required,
            decision_reasons=tuple(self.decision_reasons_json),
            materiality_overrides=tuple(
                MaterialityOverride(
                    before=item["before"],
                    after=item["after"],
                    justification=item["justification"],
                    overridden_at=datetime.fromisoformat(item["overridden_at"]),
                )
                for item in self.materiality_overrides_json
            ),
            created_at=_ensure_timezone(self.created_at),
            updated_at=_ensure_timezone(self.updated_at),
            methodology_version_id=self.methodology_version_id,
        )


class AssetValuationAssessmentModel(Base):
    __tablename__ = "asset_valuation_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"), nullable=False, index=True
    )
    exercise_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    reference_code: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True
    )
    macrogroup: Mapped[str] = mapped_column(String(80), nullable=False)
    book_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    default_desagio_percent: Mapped[Decimal] = mapped_column(
        Numeric(8, 6), nullable=False
    )
    default_economic_value: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    valuation_required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    realizability_classification: Mapped[str] = mapped_column(
        String(60), nullable=False
    )
    valuation_basis: Mapped[str] = mapped_column(String(50), nullable=False)
    forced_liquidation_value: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2), nullable=True
    )
    analyst_adjusted_value: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2), nullable=True
    )
    final_economic_value: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False
    )
    final_value_source: Mapped[str] = mapped_column(String(50), nullable=False)
    essentiality_status: Mapped[str] = mapped_column(String(30), nullable=False)
    evidence_id: Mapped[str | None] = mapped_column(
        ForeignKey("adjustment_evidences.evidence_id"),
        nullable=True,
        index=True,
    )
    valuation_status: Mapped[str] = mapped_column(
        String(30), nullable=False, index=True
    )
    blocks_plra: Mapped[bool] = mapped_column(Boolean, nullable=False, index=True)
    blocking_reasons_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    methodology_version_id: Mapped[str] = mapped_column(
        String(120), nullable=False, index=True
    )
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    def to_domain(self) -> AssetValuationAssessment:
        return AssetValuationAssessment(
            assessment_id=self.assessment_id,
            exercise_year=self.exercise_year,
            account_code=self.account_code,
            account_name=self.account_name,
            reference_code=self.reference_code,
            macrogroup=self.macrogroup,
            book_value=self.book_value,
            default_desagio_percent=self.default_desagio_percent,
            default_economic_value=self.default_economic_value,
            valuation_required=self.valuation_required,
            realizability_classification=AssetRealizability(
                self.realizability_classification
            ),
            valuation_basis=ValuationBasis(self.valuation_basis),
            forced_liquidation_value=self.forced_liquidation_value,
            analyst_adjusted_value=self.analyst_adjusted_value,
            final_economic_value=self.final_economic_value,
            final_value_source=ValuationValueSource(self.final_value_source),
            essentiality_status=EssentialityStatus(self.essentiality_status),
            evidence_id=self.evidence_id,
            valuation_status=ValuationStatus(self.valuation_status),
            blocks_plra=self.blocks_plra,
            blocking_reasons=tuple(self.blocking_reasons_json),
            methodology_version_id=self.methodology_version_id,
        )


class EvidenceNotFound(LookupError):
    pass


class AssetValuationNotFound(LookupError):
    pass


def save_adjustment_evidence(
    session: Session,
    *,
    exercise_id: int,
    evidence: AdjustmentEvidence,
) -> AdjustmentEvidenceModel:
    model = session.scalar(
        select(AdjustmentEvidenceModel).where(
            AdjustmentEvidenceModel.evidence_id == evidence.evidence_id
        )
    )
    if model is None:
        model = AdjustmentEvidenceModel(
            evidence_id=evidence.evidence_id,
            exercise_id=exercise_id,
        )
        session.add(model)
    elif model.exercise_id != exercise_id:
        raise ValueError("Evidence belongs to another exercise.")
    _assign_evidence(model, evidence)
    session.flush()
    return model


def get_adjustment_evidence(
    session: Session, *, evidence_id: str
) -> AdjustmentEvidence:
    model = session.scalar(
        select(AdjustmentEvidenceModel).where(
            AdjustmentEvidenceModel.evidence_id == evidence_id
        )
    )
    if model is None:
        raise EvidenceNotFound("Adjustment evidence not found.")
    return model.to_domain()


def list_adjustment_evidences(
    session: Session,
    *,
    exercise_id: int,
    method_component: MethodComponent | None = None,
) -> list[AdjustmentEvidence]:
    statement = select(AdjustmentEvidenceModel).where(
        AdjustmentEvidenceModel.exercise_id == exercise_id
    )
    if method_component is not None:
        statement = statement.where(
            AdjustmentEvidenceModel.method_component
            == MethodComponent(method_component).value
        )
    statement = statement.order_by(
        AdjustmentEvidenceModel.updated_at,
        AdjustmentEvidenceModel.id,
    )
    return [model.to_domain() for model in session.scalars(statement)]


def save_asset_valuation(
    session: Session,
    *,
    exercise_id: int,
    assessment: AssetValuationAssessment,
) -> AssetValuationAssessmentModel:
    model = session.scalar(
        select(AssetValuationAssessmentModel).where(
            AssetValuationAssessmentModel.assessment_id
            == assessment.assessment_id
        )
    )
    if model is None:
        model = AssetValuationAssessmentModel(
            assessment_id=assessment.assessment_id,
            exercise_id=exercise_id,
        )
        session.add(model)
    elif model.exercise_id != exercise_id:
        raise ValueError("Asset valuation belongs to another exercise.")
    _assign_asset_valuation(model, assessment)
    session.flush()
    return model


def get_asset_valuation(
    session: Session, *, assessment_id: str
) -> AssetValuationAssessment:
    model = session.scalar(
        select(AssetValuationAssessmentModel).where(
            AssetValuationAssessmentModel.assessment_id == assessment_id
        )
    )
    if model is None:
        raise AssetValuationNotFound("Asset valuation not found.")
    return model.to_domain()


def list_asset_valuations(
    session: Session, *, exercise_id: int
) -> list[AssetValuationAssessment]:
    statement = (
        select(AssetValuationAssessmentModel)
        .where(AssetValuationAssessmentModel.exercise_id == exercise_id)
        .order_by(
            AssetValuationAssessmentModel.account_code,
            AssetValuationAssessmentModel.id,
        )
    )
    return [model.to_domain() for model in session.scalars(statement)]


def _assign_evidence(
    model: AdjustmentEvidenceModel, evidence: AdjustmentEvidence
) -> None:
    model.exercise_year = evidence.exercise_year
    model.scope_type = evidence.scope_type.value
    model.scope_key = evidence.scope_key
    model.adjustment_type = evidence.adjustment_type
    model.method_component = evidence.method_component.value
    model.amount_impact = evidence.amount_impact
    model.impact_base_value = evidence.impact_base_value
    model.impact_percent = evidence.impact_percent
    model.materiality_level = evidence.materiality_level.value
    model.materiality_source = evidence.materiality_source.value
    model.minimum_materiality_level = evidence.minimum_materiality_level.value
    model.required_evidence_type = evidence.required_evidence_type
    model.evidence_status = evidence.evidence_status.value
    model.analyst_justification = evidence.analyst_justification
    model.review_notes = evidence.review_notes
    model.blocks_final_report = evidence.blocks_final_report
    model.requires_reservation = evidence.requires_reservation
    model.human_review_required = evidence.human_review_required
    model.decision_reasons_json = list(evidence.decision_reasons)
    model.materiality_overrides_json = [
        override.to_snapshot() for override in evidence.materiality_overrides
    ]
    model.methodology_version_id = evidence.methodology_version_id
    model.snapshot_json = evidence.to_snapshot()
    model.created_at = evidence.created_at
    model.updated_at = evidence.updated_at


def _assign_asset_valuation(
    model: AssetValuationAssessmentModel,
    assessment: AssetValuationAssessment,
) -> None:
    model.exercise_year = assessment.exercise_year
    model.account_code = assessment.account_code
    model.account_name = assessment.account_name
    model.reference_code = assessment.reference_code
    model.macrogroup = assessment.macrogroup
    model.book_value = assessment.book_value
    model.default_desagio_percent = assessment.default_desagio_percent
    model.default_economic_value = assessment.default_economic_value
    model.valuation_required = assessment.valuation_required
    model.realizability_classification = (
        assessment.realizability_classification.value
    )
    model.valuation_basis = assessment.valuation_basis.value
    model.forced_liquidation_value = assessment.forced_liquidation_value
    model.analyst_adjusted_value = assessment.analyst_adjusted_value
    model.final_economic_value = assessment.final_economic_value
    model.final_value_source = assessment.final_value_source.value
    model.essentiality_status = assessment.essentiality_status.value
    model.evidence_id = assessment.evidence_id
    model.valuation_status = assessment.valuation_status.value
    model.blocks_plra = assessment.blocks_plra
    model.blocking_reasons_json = list(assessment.blocking_reasons)
    model.methodology_version_id = assessment.methodology_version_id
    model.snapshot_json = assessment.to_snapshot()


def _ensure_timezone(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)

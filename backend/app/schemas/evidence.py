from __future__ import annotations

from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain import (
    AdjustmentEvidence,
    AssetRealizability,
    AssetValuationAssessment,
    EssentialityStatus,
    EvidenceScopeType,
    EvidenceStatus,
    MaterialityLevel,
    MaterialitySource,
    MethodComponent,
    ValuationBasis,
    ValuationStatus,
    ValuationValueSource,
)


class EvidenceCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope_type: EvidenceScopeType
    scope_key: str = Field(min_length=1, max_length=120)
    adjustment_type: str = Field(min_length=1, max_length=80)
    method_component: MethodComponent
    amount_impact: str
    impact_base_value: str | None = None
    required_evidence_type: str | None = None
    evidence_status: EvidenceStatus
    analyst_justification: str | None = None
    review_notes: str | None = None
    can_change_capag_status: bool = False
    can_reverse_prudential_sign: bool = False

    @model_validator(mode="after")
    def validate_contract(self) -> "EvidenceCreateRequest":
        _decimal(self.amount_impact, "amount_impact")
        _optional_decimal(self.impact_base_value, "impact_base_value")
        _validate_waiver(self.evidence_status, self.analyst_justification)
        return self


class MaterialityOverrideRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    materiality_level: MaterialityLevel
    justification: str = Field(min_length=1)


class EvidenceUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    required_evidence_type: str | None = None
    evidence_status: EvidenceStatus
    analyst_justification: str | None = None
    review_notes: str | None = None
    materiality_override: MaterialityOverrideRequest | None = None

    @model_validator(mode="after")
    def validate_waived_status(self) -> "EvidenceUpdateRequest":
        _validate_waiver(self.evidence_status, self.analyst_justification)
        return self


class EvidenceResponse(BaseModel):
    evidence_id: str
    exercise_year: int
    scope_type: EvidenceScopeType
    scope_key: str
    adjustment_type: str
    method_component: MethodComponent
    amount_impact: str
    impact_base_value: str | None
    impact_percent: str | None
    materiality_level: MaterialityLevel
    materiality_source: MaterialitySource
    minimum_materiality_level: MaterialityLevel
    required_evidence_type: str | None
    evidence_status: EvidenceStatus
    analyst_justification: str | None
    review_notes: str | None
    blocks_final_report: bool
    requires_reservation: bool
    human_review_required: bool
    decision_reasons: list[str]
    materiality_overrides: list[dict[str, str]]
    methodology_version_id: str

    @classmethod
    def from_domain(cls, evidence: AdjustmentEvidence) -> "EvidenceResponse":
        snapshot = evidence.to_snapshot()
        return cls(**{
            key: value
            for key, value in snapshot.items()
            if key not in {"created_at", "updated_at"}
        })


class ComponentEvidenceSummary(BaseModel):
    method_component: MethodComponent
    total: int
    blocking: int
    reservations: int
    pending: int


class EvidenceListResponse(BaseModel):
    items: list[EvidenceResponse]
    summaries: list[ComponentEvidenceSummary]

    @classmethod
    def from_domain(
        cls, evidences: list[AdjustmentEvidence]
    ) -> "EvidenceListResponse":
        summaries = []
        for component in MethodComponent:
            scoped = [
                evidence
                for evidence in evidences
                if evidence.method_component == component
            ]
            if scoped:
                summaries.append(
                    ComponentEvidenceSummary(
                        method_component=component,
                        total=len(scoped),
                        blocking=sum(
                            evidence.blocks_final_report
                            for evidence in scoped
                        ),
                        reservations=sum(
                            evidence.requires_reservation
                            for evidence in scoped
                        ),
                        pending=sum(
                            evidence.evidence_status
                            == EvidenceStatus.PENDING
                            for evidence in scoped
                        ),
                    )
                )
        return cls(
            items=[
                EvidenceResponse.from_domain(evidence)
                for evidence in evidences
            ],
            summaries=summaries,
        )


class AssetValuationUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis_id: str = Field(min_length=1, max_length=64)
    exercise_year: int = Field(ge=1)
    account_code: str = Field(min_length=1, max_length=64)
    realizability_classification: AssetRealizability
    valuation_required: bool
    valuation_basis: ValuationBasis
    forced_liquidation_value: str | None = None
    analyst_adjusted_value: str | None = None
    essentiality_status: EssentialityStatus
    valuation_status: ValuationStatus
    evidence_id: str | None = None

    @model_validator(mode="after")
    def validate_values(self) -> "AssetValuationUpdateRequest":
        _optional_decimal(
            self.forced_liquidation_value, "forced_liquidation_value"
        )
        _optional_decimal(
            self.analyst_adjusted_value, "analyst_adjusted_value"
        )
        if (
            self.forced_liquidation_value is not None
            and self.analyst_adjusted_value is not None
        ):
            raise ValueError(
                "forced_liquidation_value and analyst_adjusted_value "
                "cannot be informed together"
            )
        return self


class AssetValuationResponse(BaseModel):
    assessment_id: str
    exercise_year: int
    account_code: str
    account_name: str
    reference_code: str
    macrogroup: str
    book_value: str
    default_desagio_percent: str
    default_economic_value: str
    valuation_required: bool
    realizability_classification: AssetRealizability
    valuation_basis: ValuationBasis
    forced_liquidation_value: str | None
    analyst_adjusted_value: str | None
    final_economic_value: str
    final_value_source: ValuationValueSource
    essentiality_status: EssentialityStatus
    evidence_id: str | None
    valuation_status: ValuationStatus
    blocks_plra: bool
    blocking_reasons: list[str]
    methodology_version_id: str

    @classmethod
    def from_domain(
        cls, assessment: AssetValuationAssessment
    ) -> "AssetValuationResponse":
        return cls(**assessment.to_snapshot())


class AssetValuationListResponse(BaseModel):
    items: list[AssetValuationResponse]
    blocking_count: int

    @classmethod
    def from_domain(
        cls, assessments: list[AssetValuationAssessment]
    ) -> "AssetValuationListResponse":
        return cls(
            items=[
                AssetValuationResponse.from_domain(assessment)
                for assessment in assessments
            ],
            blocking_count=sum(
                assessment.blocks_plra for assessment in assessments
            ),
        )


class EvidenceApiErrorResponse(BaseModel):
    error_code: str
    message: str


def _decimal(value: str, field_name: str) -> Decimal:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{field_name} must be a decimal string") from exc
    if not parsed.is_finite():
        raise ValueError(f"{field_name} must be a finite decimal string")
    return parsed


def _optional_decimal(value: str | None, field_name: str) -> Decimal | None:
    return None if value is None else _decimal(value, field_name)


def _validate_waiver(
    status: EvidenceStatus, justification: str | None
) -> None:
    if (
        status == EvidenceStatus.WAIVED_WITH_JUSTIFICATION
        and (justification is None or not justification.strip())
    ):
        raise ValueError("waived evidence requires analyst justification")

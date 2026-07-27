from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from app.domain.capag import CENT


PERCENT_PRECISION = Decimal("0.000001")


class EvidenceScopeType(StrEnum):
    ACCOUNT = "account"
    METHODOLOGY_GROUP = "methodology_group"
    MACROGROUP = "macrogroup"
    FCO_MOVEMENT = "fco_movement"
    DFC_COMPONENT = "dfc_component"
    ROA_COMPONENT = "roa_component"
    ASSET_VALUATION = "asset_valuation"
    MANUAL_OVERRIDE = "manual_override"
    CAPAG_ASSESSMENT = "capag_assessment"


class MethodComponent(StrEnum):
    PLRA = "PLRA"
    FCA = "FCA"
    ROA = "ROA"
    CAPAG_E = "CAPAG-E"


class EvidenceStatus(StrEnum):
    NOT_REQUIRED = "nao_exigida"
    PENDING = "pendente"
    INFORMED = "informada"
    VALIDATED = "validada"
    WAIVED_WITH_JUSTIFICATION = "dispensada_com_justificativa"
    REJECTED = "rejeitada"


class MaterialityLevel(StrEnum):
    LOW = "baixa"
    MEDIUM = "media"
    HIGH = "alta"
    CRITICAL = "critica"


class MaterialitySource(StrEnum):
    DEFAULT_POLICY = "politica_default"
    MANUAL_OVERRIDE = "override_manual"


class AssetRealizability(StrEnum):
    IMMEDIATE_LIQUIDITY = "liquidez_imediata"
    SHORT_TERM = "realizavel_curto_prazo"
    LONG_TERM = "realizavel_longo_prazo"
    FORCED_LIQUIDATION_REQUIRES_REPORT = "liquidacao_forcada_exige_laudo"
    ESSENTIAL_OPERATING_ASSET = "ativo_operacional_essencial"
    NO_REALIZABILITY = "ativo_sem_realizabilidade"
    CONDITIONAL_ASSET = "ativo_condicional"


class ValuationBasis(StrEnum):
    INTERNAL_POLICY = "politica_interna"
    ABNT_NBR_14653_REPORT = "laudo_abnt_nbr_14653"
    SUPPORTING_DOCUMENT = "documento_suporte"
    ANALYST_ESTIMATE = "estimativa_analista"
    NOT_APPLICABLE = "nao_aplicavel"


class EssentialityStatus(StrEnum):
    NOT_ESSENTIAL = "nao_essencial"
    ESSENTIAL = "essencial"
    UNDER_REVIEW = "em_revisao"


class ValuationStatus(StrEnum):
    NOT_REQUIRED = "nao_exigida"
    PENDING = "pendente"
    VALIDATED = "validada"
    REJECTED = "rejeitada"
    BLOCKING = "bloqueante"


class ValuationValueSource(StrEnum):
    DEFAULT_POLICY = "politica_default"
    FORCED_LIQUIDATION = "liquidacao_forcada_validada"
    ANALYST_ADJUSTMENT = "ajuste_analista_validado"
    ZERO_REALIZABILITY = "sem_realizabilidade"


@dataclass(frozen=True)
class MaterialityOverride:
    before: MaterialityLevel
    after: MaterialityLevel
    justification: str
    overridden_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "before", MaterialityLevel(self.before))
        object.__setattr__(self, "after", MaterialityLevel(self.after))
        if not self.justification.strip():
            raise ValueError("Materiality override justification is required.")

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "before": self.before.value,
            "after": self.after.value,
            "justification": self.justification,
            "overridden_at": self.overridden_at.isoformat(),
        }


@dataclass(frozen=True)
class AdjustmentEvidence:
    evidence_id: str
    exercise_year: int
    scope_type: EvidenceScopeType
    scope_key: str
    adjustment_type: str
    method_component: MethodComponent
    amount_impact: Decimal
    impact_base_value: Decimal | None
    impact_percent: Decimal | None
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
    decision_reasons: tuple[str, ...]
    materiality_overrides: tuple[MaterialityOverride, ...]
    created_at: datetime
    updated_at: datetime
    methodology_version_id: str

    def __post_init__(self) -> None:
        for field_name in {
            "evidence_id",
            "scope_key",
            "adjustment_type",
            "methodology_version_id",
        }:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} is required.")
        if isinstance(self.exercise_year, bool) or not isinstance(
            self.exercise_year, int
        ):
            raise TypeError("exercise_year must be int.")
        if self.exercise_year < 1:
            raise ValueError("exercise_year must be positive.")

        object.__setattr__(self, "scope_type", EvidenceScopeType(self.scope_type))
        object.__setattr__(
            self, "method_component", MethodComponent(self.method_component)
        )
        object.__setattr__(
            self, "materiality_level", MaterialityLevel(self.materiality_level)
        )
        object.__setattr__(
            self,
            "materiality_source",
            MaterialitySource(self.materiality_source),
        )
        object.__setattr__(
            self,
            "minimum_materiality_level",
            MaterialityLevel(self.minimum_materiality_level),
        )
        object.__setattr__(
            self, "evidence_status", EvidenceStatus(self.evidence_status)
        )
        object.__setattr__(
            self,
            "amount_impact",
            _quantize_decimal("amount_impact", self.amount_impact, CENT),
        )
        if self.impact_base_value is not None:
            object.__setattr__(
                self,
                "impact_base_value",
                _quantize_decimal(
                    "impact_base_value", self.impact_base_value, CENT
                ),
            )
        if self.impact_percent is not None:
            percent = _quantize_decimal(
                "impact_percent", self.impact_percent, PERCENT_PRECISION
            )
            if percent < Decimal("0"):
                raise ValueError("impact_percent cannot be negative.")
            object.__setattr__(self, "impact_percent", percent)
        object.__setattr__(
            self, "decision_reasons", tuple(self.decision_reasons)
        )
        object.__setattr__(
            self, "materiality_overrides", tuple(self.materiality_overrides)
        )
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot precede created_at.")

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "exercise_year": self.exercise_year,
            "scope_type": self.scope_type.value,
            "scope_key": self.scope_key,
            "adjustment_type": self.adjustment_type,
            "method_component": self.method_component.value,
            "amount_impact": format(self.amount_impact, "f"),
            "impact_base_value": _decimal_string(self.impact_base_value),
            "impact_percent": _decimal_string(self.impact_percent),
            "materiality_level": self.materiality_level.value,
            "materiality_source": self.materiality_source.value,
            "minimum_materiality_level": self.minimum_materiality_level.value,
            "required_evidence_type": self.required_evidence_type,
            "evidence_status": self.evidence_status.value,
            "analyst_justification": self.analyst_justification,
            "review_notes": self.review_notes,
            "blocks_final_report": self.blocks_final_report,
            "requires_reservation": self.requires_reservation,
            "human_review_required": self.human_review_required,
            "decision_reasons": list(self.decision_reasons),
            "materiality_overrides": [
                override.to_snapshot() for override in self.materiality_overrides
            ],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "methodology_version_id": self.methodology_version_id,
        }


@dataclass(frozen=True)
class AssetValuationAssessment:
    assessment_id: str
    exercise_year: int
    account_code: str
    account_name: str
    reference_code: str
    macrogroup: str
    book_value: Decimal
    default_desagio_percent: Decimal
    default_economic_value: Decimal
    valuation_required: bool
    realizability_classification: AssetRealizability
    valuation_basis: ValuationBasis
    forced_liquidation_value: Decimal | None
    analyst_adjusted_value: Decimal | None
    final_economic_value: Decimal
    final_value_source: ValuationValueSource
    essentiality_status: EssentialityStatus
    evidence_id: str | None
    valuation_status: ValuationStatus
    blocks_plra: bool
    blocking_reasons: tuple[str, ...]
    methodology_version_id: str

    def __post_init__(self) -> None:
        for field_name in {
            "assessment_id",
            "account_code",
            "account_name",
            "reference_code",
            "macrogroup",
            "methodology_version_id",
        }:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} is required.")
        if isinstance(self.exercise_year, bool) or not isinstance(
            self.exercise_year, int
        ):
            raise TypeError("exercise_year must be int.")
        if self.exercise_year < 1:
            raise ValueError("exercise_year must be positive.")
        for field_name in {
            "book_value",
            "default_economic_value",
            "forced_liquidation_value",
            "analyst_adjusted_value",
            "final_economic_value",
        }:
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(
                    self,
                    field_name,
                    _quantize_decimal(field_name, value, CENT),
                )
        discount = _quantize_decimal(
            "default_desagio_percent",
            self.default_desagio_percent,
            PERCENT_PRECISION,
        )
        if discount < Decimal("0") or discount > Decimal("1"):
            raise ValueError(
                "default_desagio_percent must be between zero and one."
            )
        object.__setattr__(self, "default_desagio_percent", discount)
        object.__setattr__(
            self,
            "realizability_classification",
            AssetRealizability(self.realizability_classification),
        )
        object.__setattr__(
            self, "valuation_basis", ValuationBasis(self.valuation_basis)
        )
        object.__setattr__(
            self,
            "final_value_source",
            ValuationValueSource(self.final_value_source),
        )
        object.__setattr__(
            self,
            "essentiality_status",
            EssentialityStatus(self.essentiality_status),
        )
        object.__setattr__(
            self, "valuation_status", ValuationStatus(self.valuation_status)
        )
        object.__setattr__(
            self, "blocking_reasons", tuple(self.blocking_reasons)
        )

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "assessment_id": self.assessment_id,
            "exercise_year": self.exercise_year,
            "account_code": self.account_code,
            "account_name": self.account_name,
            "reference_code": self.reference_code,
            "macrogroup": self.macrogroup,
            "book_value": format(self.book_value, "f"),
            "default_desagio_percent": format(
                self.default_desagio_percent, "f"
            ),
            "default_economic_value": format(
                self.default_economic_value, "f"
            ),
            "valuation_required": self.valuation_required,
            "realizability_classification": (
                self.realizability_classification.value
            ),
            "valuation_basis": self.valuation_basis.value,
            "forced_liquidation_value": _decimal_string(
                self.forced_liquidation_value
            ),
            "analyst_adjusted_value": _decimal_string(
                self.analyst_adjusted_value
            ),
            "final_economic_value": format(self.final_economic_value, "f"),
            "final_value_source": self.final_value_source.value,
            "essentiality_status": self.essentiality_status.value,
            "evidence_id": self.evidence_id,
            "valuation_status": self.valuation_status.value,
            "blocks_plra": self.blocks_plra,
            "blocking_reasons": list(self.blocking_reasons),
            "methodology_version_id": self.methodology_version_id,
        }


def _quantize_decimal(
    field_name: str, value: object, precision: Decimal
) -> Decimal:
    if not isinstance(value, Decimal):
        raise TypeError(f"{field_name} must be Decimal.")
    if not value.is_finite():
        raise ValueError(f"{field_name} must be finite.")
    return value.quantize(precision)


def _decimal_string(value: Decimal | None) -> str | None:
    return None if value is None else format(value, "f")

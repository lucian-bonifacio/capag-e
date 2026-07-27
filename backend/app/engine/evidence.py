from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal

from app.domain.evidence import (
    AdjustmentEvidence,
    EvidenceScopeType,
    EvidenceStatus,
    MaterialityLevel,
    MaterialityOverride,
    MaterialitySource,
    MethodComponent,
)


LOW_THRESHOLD = Decimal("0.01")
MEDIUM_THRESHOLD = Decimal("0.05")
HIGH_THRESHOLD = Decimal("0.10")
MATERIALITY_POLICY_VERSION = "materiality-default-v1"

_LEVEL_RANK = {
    MaterialityLevel.LOW: 0,
    MaterialityLevel.MEDIUM: 1,
    MaterialityLevel.HIGH: 2,
    MaterialityLevel.CRITICAL: 3,
}


@dataclass(frozen=True)
class MaterialityDecision:
    impact_percent: Decimal | None
    materiality_level: MaterialityLevel
    minimum_materiality_level: MaterialityLevel
    human_review_required: bool
    reasons: tuple[str, ...]
    policy_version_id: str = MATERIALITY_POLICY_VERSION


@dataclass(frozen=True)
class EvidenceDisposition:
    blocks_final_report: bool
    requires_reservation: bool
    reasons: tuple[str, ...]


def calculate_default_materiality(
    *,
    amount_impact: Decimal,
    impact_base_value: Decimal | None,
    can_change_capag_status: bool = False,
    can_reverse_prudential_sign: bool = False,
) -> MaterialityDecision:
    _validate_decimal("amount_impact", amount_impact)
    if impact_base_value is not None:
        _validate_decimal("impact_base_value", impact_base_value)

    reasons: list[str] = []
    human_review_required = False
    minimum_level = MaterialityLevel.LOW

    if impact_base_value is None or impact_base_value <= Decimal("0"):
        impact_percent = None
        level = MaterialityLevel.MEDIUM
        minimum_level = MaterialityLevel.MEDIUM
        human_review_required = True
        reasons.append("BASE_PERCENTUAL_INVALIDA_REVISAO_OBRIGATORIA")
    else:
        impact_percent = abs(amount_impact) / abs(impact_base_value)
        level = _level_for_percent(impact_percent)
        reasons.append(f"FAIXA_DEFAULT_{level.value.upper()}")

    if can_change_capag_status:
        level = _raise_to(level, MaterialityLevel.HIGH)
        minimum_level = _raise_to(minimum_level, MaterialityLevel.HIGH)
        human_review_required = True
        reasons.append("PODE_ALTERAR_STATUS_CAPAG_E")
    if can_reverse_prudential_sign:
        level = _raise_to(level, MaterialityLevel.HIGH)
        minimum_level = _raise_to(minimum_level, MaterialityLevel.HIGH)
        human_review_required = True
        reasons.append("PODE_INVERTER_SINAL_PRUDENCIAL")

    return MaterialityDecision(
        impact_percent=impact_percent,
        materiality_level=level,
        minimum_materiality_level=minimum_level,
        human_review_required=human_review_required,
        reasons=tuple(reasons),
    )


def build_adjustment_evidence(
    *,
    evidence_id: str,
    exercise_year: int,
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
    methodology_version_id: str,
    can_change_capag_status: bool = False,
    can_reverse_prudential_sign: bool = False,
    created_at: datetime | None = None,
) -> AdjustmentEvidence:
    decision = calculate_default_materiality(
        amount_impact=amount_impact,
        impact_base_value=impact_base_value,
        can_change_capag_status=can_change_capag_status,
        can_reverse_prudential_sign=can_reverse_prudential_sign,
    )
    disposition = evaluate_evidence_disposition(
        materiality_level=decision.materiality_level,
        evidence_status=evidence_status,
        required_evidence_type=required_evidence_type,
        analyst_justification=analyst_justification,
    )
    timestamp = created_at or datetime.now(timezone.utc)
    return AdjustmentEvidence(
        evidence_id=evidence_id,
        exercise_year=exercise_year,
        scope_type=scope_type,
        scope_key=scope_key,
        adjustment_type=adjustment_type,
        method_component=method_component,
        amount_impact=amount_impact,
        impact_base_value=impact_base_value,
        impact_percent=decision.impact_percent,
        materiality_level=decision.materiality_level,
        materiality_source=MaterialitySource.DEFAULT_POLICY,
        minimum_materiality_level=decision.minimum_materiality_level,
        required_evidence_type=required_evidence_type,
        evidence_status=evidence_status,
        analyst_justification=analyst_justification,
        review_notes=review_notes,
        blocks_final_report=disposition.blocks_final_report,
        requires_reservation=disposition.requires_reservation,
        human_review_required=decision.human_review_required,
        decision_reasons=decision.reasons + disposition.reasons,
        materiality_overrides=(),
        created_at=timestamp,
        updated_at=timestamp,
        methodology_version_id=methodology_version_id,
    )


def apply_materiality_override(
    evidence: AdjustmentEvidence,
    *,
    materiality_level: MaterialityLevel,
    justification: str,
    overridden_at: datetime | None = None,
) -> AdjustmentEvidence:
    target_level = MaterialityLevel(materiality_level)
    if not justification.strip():
        raise ValueError("Materiality override justification is required.")
    if _LEVEL_RANK[target_level] < _LEVEL_RANK[evidence.minimum_materiality_level]:
        raise ValueError(
            "Materiality override cannot violate the conservative minimum."
        )

    timestamp = overridden_at or datetime.now(timezone.utc)
    override = MaterialityOverride(
        before=evidence.materiality_level,
        after=target_level,
        justification=justification,
        overridden_at=timestamp,
    )
    disposition = evaluate_evidence_disposition(
        materiality_level=target_level,
        evidence_status=evidence.evidence_status,
        required_evidence_type=evidence.required_evidence_type,
        analyst_justification=evidence.analyst_justification,
    )
    non_disposition_reasons = tuple(
        reason
        for reason in evidence.decision_reasons
        if not reason.startswith("EVIDENCIA_")
        and not reason.startswith("JUSTIFICATIVA_")
        and not reason.startswith("TIPO_EVIDENCIA_")
    )
    return replace(
        evidence,
        materiality_level=target_level,
        materiality_source=MaterialitySource.MANUAL_OVERRIDE,
        blocks_final_report=disposition.blocks_final_report,
        requires_reservation=disposition.requires_reservation,
        decision_reasons=non_disposition_reasons
        + (f"OVERRIDE_MATERIALIDADE:{justification.strip()}",)
        + disposition.reasons,
        materiality_overrides=evidence.materiality_overrides + (override,),
        updated_at=timestamp,
    )


def revise_adjustment_evidence(
    evidence: AdjustmentEvidence,
    *,
    evidence_status: EvidenceStatus,
    required_evidence_type: str | None,
    analyst_justification: str | None,
    review_notes: str | None,
    updated_at: datetime | None = None,
) -> AdjustmentEvidence:
    status = EvidenceStatus(evidence_status)
    disposition = evaluate_evidence_disposition(
        materiality_level=evidence.materiality_level,
        evidence_status=status,
        required_evidence_type=required_evidence_type,
        analyst_justification=analyst_justification,
    )
    non_disposition_reasons = tuple(
        reason
        for reason in evidence.decision_reasons
        if not reason.startswith("EVIDENCIA_")
        and not reason.startswith("JUSTIFICATIVA_")
        and not reason.startswith("TIPO_EVIDENCIA_")
    )
    return replace(
        evidence,
        required_evidence_type=required_evidence_type,
        evidence_status=status,
        analyst_justification=analyst_justification,
        review_notes=review_notes,
        blocks_final_report=disposition.blocks_final_report,
        requires_reservation=disposition.requires_reservation,
        decision_reasons=non_disposition_reasons + disposition.reasons,
        updated_at=updated_at or datetime.now(timezone.utc),
    )


def evaluate_evidence_disposition(
    *,
    materiality_level: MaterialityLevel,
    evidence_status: EvidenceStatus,
    required_evidence_type: str | None,
    analyst_justification: str | None,
) -> EvidenceDisposition:
    level = MaterialityLevel(materiality_level)
    status = EvidenceStatus(evidence_status)
    material = level != MaterialityLevel.LOW
    high_or_critical = level in {
        MaterialityLevel.HIGH,
        MaterialityLevel.CRITICAL,
    }
    blocks = False
    reservation = False
    reasons: list[str] = []

    if status == EvidenceStatus.REJECTED:
        blocks = True
        reasons.append("EVIDENCIA_REJEITADA")
    elif status == EvidenceStatus.PENDING:
        blocks = high_or_critical
        reservation = not blocks
        reasons.append("EVIDENCIA_PENDENTE")
    elif status == EvidenceStatus.INFORMED:
        reservation = True
        reasons.append("EVIDENCIA_INFORMADA_NAO_VALIDADA")
    elif (
        status == EvidenceStatus.WAIVED_WITH_JUSTIFICATION
        and not _has_text(analyst_justification)
    ):
        blocks = high_or_critical
        reservation = not blocks
        reasons.append("EVIDENCIA_DISPENSADA_SEM_JUSTIFICATIVA")

    if material and not _has_text(analyst_justification):
        if high_or_critical:
            blocks = True
        else:
            reservation = True
        reasons.append("JUSTIFICATIVA_MATERIAL_AUSENTE")

    if material and not _has_text(required_evidence_type):
        if high_or_critical:
            blocks = True
        else:
            reservation = True
        reasons.append("TIPO_EVIDENCIA_MATERIAL_AUSENTE")

    return EvidenceDisposition(
        blocks_final_report=blocks,
        requires_reservation=reservation,
        reasons=tuple(dict.fromkeys(reasons)),
    )


def _level_for_percent(impact_percent: Decimal) -> MaterialityLevel:
    if impact_percent < LOW_THRESHOLD:
        return MaterialityLevel.LOW
    if impact_percent < MEDIUM_THRESHOLD:
        return MaterialityLevel.MEDIUM
    if impact_percent < HIGH_THRESHOLD:
        return MaterialityLevel.HIGH
    return MaterialityLevel.CRITICAL


def _raise_to(
    current: MaterialityLevel, minimum: MaterialityLevel
) -> MaterialityLevel:
    return (
        minimum
        if _LEVEL_RANK[current] < _LEVEL_RANK[minimum]
        else current
    )


def _validate_decimal(field_name: str, value: object) -> None:
    if not isinstance(value, Decimal):
        raise TypeError(f"{field_name} must be Decimal.")
    if not value.is_finite():
        raise ValueError(f"{field_name} must be finite.")


def _has_text(value: str | None) -> bool:
    return value is not None and bool(value.strip())

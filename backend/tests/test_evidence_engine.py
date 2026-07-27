from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.domain.evidence import (
    EvidenceScopeType,
    EvidenceStatus,
    MaterialityLevel,
    MaterialitySource,
    MethodComponent,
)
from app.engine.evidence import (
    apply_materiality_override,
    build_adjustment_evidence,
    calculate_default_materiality,
    evaluate_evidence_disposition,
)


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("9.99", MaterialityLevel.LOW),
        ("10.00", MaterialityLevel.MEDIUM),
        ("49.99", MaterialityLevel.MEDIUM),
        ("50.00", MaterialityLevel.HIGH),
        ("99.99", MaterialityLevel.HIGH),
        ("100.00", MaterialityLevel.CRITICAL),
    ],
)
def test_materiality_uses_governed_boundaries(
    amount: str, expected: MaterialityLevel
) -> None:
    decision = calculate_default_materiality(
        amount_impact=Decimal(amount),
        impact_base_value=Decimal("1000.00"),
    )

    assert decision.materiality_level == expected


@pytest.mark.parametrize("base", [None, Decimal("0.00"), Decimal("-1.00")])
def test_invalid_base_forces_medium_and_human_review(
    base: Decimal | None,
) -> None:
    decision = calculate_default_materiality(
        amount_impact=Decimal("1.00"),
        impact_base_value=base,
    )

    assert decision.impact_percent is None
    assert decision.materiality_level == MaterialityLevel.MEDIUM
    assert decision.minimum_materiality_level == MaterialityLevel.MEDIUM
    assert decision.human_review_required is True


@pytest.mark.parametrize(
    "conservative_flag",
    ["can_change_capag_status", "can_reverse_prudential_sign"],
)
def test_conservative_events_force_high_materiality(
    conservative_flag: str,
) -> None:
    flags = {conservative_flag: True}

    decision = calculate_default_materiality(
        amount_impact=Decimal("1.00"),
        impact_base_value=Decimal("1000.00"),
        **flags,
    )

    assert decision.materiality_level == MaterialityLevel.HIGH
    assert decision.minimum_materiality_level == MaterialityLevel.HIGH
    assert decision.human_review_required is True


def test_critical_pending_evidence_blocks_final_report() -> None:
    evidence = _build_evidence(
        amount_impact=Decimal("100.00"),
        evidence_status=EvidenceStatus.PENDING,
    )

    assert evidence.materiality_level == MaterialityLevel.CRITICAL
    assert evidence.blocks_final_report is True
    assert evidence.requires_reservation is False


def test_medium_pending_evidence_requires_reservation() -> None:
    disposition = evaluate_evidence_disposition(
        materiality_level=MaterialityLevel.MEDIUM,
        evidence_status=EvidenceStatus.PENDING,
        required_evidence_type="documento_suporte",
        analyst_justification="Ajuste identificado na conciliacao.",
    )

    assert disposition.blocks_final_report is False
    assert disposition.requires_reservation is True


def test_waived_evidence_with_justification_is_not_blocking() -> None:
    evidence = _build_evidence(
        amount_impact=Decimal("100.00"),
        evidence_status=EvidenceStatus.WAIVED_WITH_JUSTIFICATION,
    )

    assert evidence.blocks_final_report is False
    assert evidence.requires_reservation is False


def test_rejected_evidence_is_always_blocking() -> None:
    disposition = evaluate_evidence_disposition(
        materiality_level=MaterialityLevel.LOW,
        evidence_status=EvidenceStatus.REJECTED,
        required_evidence_type=None,
        analyst_justification=None,
    )

    assert disposition.blocks_final_report is True


def test_material_adjustment_without_justification_and_type_is_flagged() -> None:
    evidence = _build_evidence(
        amount_impact=Decimal("50.00"),
        evidence_status=EvidenceStatus.NOT_REQUIRED,
        required_evidence_type=None,
        analyst_justification=None,
    )

    assert evidence.materiality_level == MaterialityLevel.HIGH
    assert evidence.blocks_final_report is True
    assert "JUSTIFICATIVA_MATERIAL_AUSENTE" in evidence.decision_reasons
    assert "TIPO_EVIDENCIA_MATERIAL_AUSENTE" in evidence.decision_reasons


def test_override_requires_justification_and_records_before_after() -> None:
    evidence = _build_evidence(amount_impact=Decimal("50.00"))

    with pytest.raises(
        ValueError, match="override justification is required"
    ):
        apply_materiality_override(
            evidence,
            materiality_level=MaterialityLevel.MEDIUM,
            justification=" ",
        )

    overridden = apply_materiality_override(
        evidence,
        materiality_level=MaterialityLevel.MEDIUM,
        justification="Documentacao reduz o risco efetivo.",
        overridden_at=datetime(2026, 7, 24, tzinfo=timezone.utc),
    )

    assert overridden.materiality_source == MaterialitySource.MANUAL_OVERRIDE
    assert overridden.materiality_level == MaterialityLevel.MEDIUM
    assert overridden.materiality_overrides[0].before == MaterialityLevel.HIGH
    assert overridden.materiality_overrides[0].after == MaterialityLevel.MEDIUM
    assert overridden.amount_impact == evidence.amount_impact
    assert overridden.impact_base_value == evidence.impact_base_value


def test_override_cannot_break_conservative_minimum() -> None:
    evidence = _build_evidence(
        amount_impact=Decimal("1.00"),
        can_change_capag_status=True,
    )

    with pytest.raises(ValueError, match="conservative minimum"):
        apply_materiality_override(
            evidence,
            materiality_level=MaterialityLevel.MEDIUM,
            justification="Tentativa de reducao.",
        )


def test_float_is_rejected() -> None:
    with pytest.raises(TypeError, match="amount_impact must be Decimal"):
        calculate_default_materiality(
            amount_impact=1.0,  # type: ignore[arg-type]
            impact_base_value=Decimal("100.00"),
        )


def test_snapshot_serializes_decimals_and_keeps_adjustment_value() -> None:
    evidence = _build_evidence(amount_impact=Decimal("-10.125"))

    snapshot = evidence.to_snapshot()

    assert snapshot["amount_impact"] == "-10.12"
    assert snapshot["impact_base_value"] == "1000.00"
    assert snapshot["impact_percent"] == "0.010125"
    assert snapshot["materiality_level"] == "media"


def _build_evidence(
    *,
    amount_impact: Decimal,
    evidence_status: EvidenceStatus = EvidenceStatus.VALIDATED,
    required_evidence_type: str | None = "documento_suporte",
    analyst_justification: str | None = "Ajuste conciliado pelo analista.",
    can_change_capag_status: bool = False,
):
    return build_adjustment_evidence(
        evidence_id="evidence-1",
        exercise_year=2024,
        scope_type=EvidenceScopeType.ACCOUNT,
        scope_key="1.1.01",
        adjustment_type="reclassificacao",
        method_component=MethodComponent.PLRA,
        amount_impact=amount_impact,
        impact_base_value=Decimal("1000.00"),
        required_evidence_type=required_evidence_type,
        evidence_status=evidence_status,
        analyst_justification=analyst_justification,
        review_notes=None,
        methodology_version_id="plra-v1",
        can_change_capag_status=can_change_capag_status,
        created_at=datetime(2026, 7, 24, tzinfo=timezone.utc),
    )

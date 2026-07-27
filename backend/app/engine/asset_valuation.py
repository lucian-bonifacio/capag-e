from __future__ import annotations

from decimal import Decimal

from app.assets.methodology import PlraPolicy
from app.domain.capag import CENT
from app.domain.evidence import (
    AdjustmentEvidence,
    AssetRealizability,
    AssetValuationAssessment,
    EssentialityStatus,
    EvidenceStatus,
    ValuationBasis,
    ValuationStatus,
    ValuationValueSource,
)


ONE = Decimal("1")
ZERO = Decimal("0.00")


def assess_asset_valuation(
    *,
    assessment_id: str,
    exercise_year: int,
    account_code: str,
    account_name: str,
    reference_code: str,
    book_value: Decimal,
    policy: PlraPolicy,
    realizability_classification: AssetRealizability,
    valuation_required: bool,
    valuation_basis: ValuationBasis,
    forced_liquidation_value: Decimal | None,
    analyst_adjusted_value: Decimal | None,
    essentiality_status: EssentialityStatus,
    valuation_status: ValuationStatus,
    evidence: AdjustmentEvidence | None,
) -> AssetValuationAssessment:
    _validate_decimal("book_value", book_value)
    _validate_optional_decimal(
        "forced_liquidation_value", forced_liquidation_value
    )
    _validate_optional_decimal(
        "analyst_adjusted_value", analyst_adjusted_value
    )
    if (
        forced_liquidation_value is not None
        and analyst_adjusted_value is not None
    ):
        raise ValueError(
            "Forced liquidation and analyst values cannot be informed together."
        )

    rule = policy.rule_for(reference_code, exercise_year)
    if (
        rule is None
        or rule.rule_status != "ATIVA"
        or rule.treatment != "INCLUIR_ATIVO"
        or rule.default_discount_group is None
    ):
        raise ValueError(
            "Asset valuation requires an active exact PLRA asset rule."
        )
    discount = policy.default_discounts[rule.default_discount_group]
    default_value = (book_value * (ONE - discount)).quantize(CENT)
    classification = AssetRealizability(realizability_classification)
    basis = ValuationBasis(valuation_basis)
    essentiality = EssentialityStatus(essentiality_status)
    status = ValuationStatus(valuation_status)

    final_value = default_value
    final_source = ValuationValueSource.DEFAULT_POLICY
    blocking_reasons: list[str] = []
    evidence_valid = _has_validated_evidence(evidence)

    is_essential = (
        essentiality == EssentialityStatus.ESSENTIAL
        or classification == AssetRealizability.ESSENTIAL_OPERATING_ASSET
    )
    if classification == AssetRealizability.NO_REALIZABILITY:
        if is_essential:
            blocking_reasons.append(
                "ATIVO_ESSENCIAL_SEM_REALIZABILIDADE_EXIGE_REVISAO"
            )
        else:
            final_value = ZERO
            final_source = ValuationValueSource.ZERO_REALIZABILITY
            basis = ValuationBasis.NOT_APPLICABLE

    if forced_liquidation_value is not None:
        if (
            status == ValuationStatus.VALIDATED
            and evidence_valid
            and basis
            in {
                ValuationBasis.ABNT_NBR_14653_REPORT,
                ValuationBasis.SUPPORTING_DOCUMENT,
            }
        ):
            final_value = forced_liquidation_value
            final_source = ValuationValueSource.FORCED_LIQUIDATION
        else:
            blocking_reasons.append(
                "LIQUIDACAO_FORCADA_SEM_VALIDACAO_DOCUMENTAL"
            )

    if analyst_adjusted_value is not None:
        if (
            status == ValuationStatus.VALIDATED
            and evidence_valid
            and _has_text(evidence.analyst_justification if evidence else None)
            and basis == ValuationBasis.ANALYST_ESTIMATE
        ):
            final_value = analyst_adjusted_value
            final_source = ValuationValueSource.ANALYST_ADJUSTMENT
        else:
            blocking_reasons.append(
                "VALOR_MANUAL_SEM_JUSTIFICATIVA_E_EVIDENCIA_VALIDADA"
            )

    if (
        classification
        == AssetRealizability.FORCED_LIQUIDATION_REQUIRES_REPORT
        and final_source != ValuationValueSource.FORCED_LIQUIDATION
    ):
        blocking_reasons.append("ATIVO_MATERIAL_SEM_LAUDO_VALIDADO")
    if valuation_required and status != ValuationStatus.VALIDATED:
        blocking_reasons.append("AVALIACAO_OBRIGATORIA_NAO_VALIDADA")
    if status in {ValuationStatus.REJECTED, ValuationStatus.BLOCKING}:
        blocking_reasons.append(f"AVALIACAO_{status.value.upper()}")
    if (
        is_essential
        and final_value == ZERO
        and final_source
        not in {
            ValuationValueSource.FORCED_LIQUIDATION,
            ValuationValueSource.ANALYST_ADJUSTMENT,
        }
    ):
        blocking_reasons.append("ATIVO_ESSENCIAL_NAO_PODE_SER_EXCLUIDO")

    return AssetValuationAssessment(
        assessment_id=assessment_id,
        exercise_year=exercise_year,
        account_code=account_code,
        account_name=account_name,
        reference_code=reference_code,
        macrogroup=rule.macrogroup,
        book_value=book_value,
        default_desagio_percent=discount,
        default_economic_value=default_value,
        valuation_required=valuation_required,
        realizability_classification=classification,
        valuation_basis=basis,
        forced_liquidation_value=forced_liquidation_value,
        analyst_adjusted_value=analyst_adjusted_value,
        final_economic_value=final_value,
        final_value_source=final_source,
        essentiality_status=essentiality,
        evidence_id=evidence.evidence_id if evidence is not None else None,
        valuation_status=status,
        blocks_plra=bool(blocking_reasons),
        blocking_reasons=tuple(dict.fromkeys(blocking_reasons)),
        methodology_version_id=policy.methodology_version_id,
    )


def _has_validated_evidence(
    evidence: AdjustmentEvidence | None,
) -> bool:
    return (
        evidence is not None
        and evidence.evidence_status == EvidenceStatus.VALIDATED
    )


def _validate_optional_decimal(field_name: str, value: object) -> None:
    if value is not None:
        _validate_decimal(field_name, value)


def _validate_decimal(field_name: str, value: object) -> None:
    if not isinstance(value, Decimal):
        raise TypeError(f"{field_name} must be Decimal.")
    if not value.is_finite():
        raise ValueError(f"{field_name} must be finite.")


def _has_text(value: str | None) -> bool:
    return value is not None and bool(value.strip())

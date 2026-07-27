from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.assets.methodology import load_plra_policy
from app.domain.evidence import (
    AssetRealizability,
    EssentialityStatus,
    EvidenceScopeType,
    EvidenceStatus,
    MethodComponent,
    ValuationBasis,
    ValuationStatus,
    ValuationValueSource,
)
from app.engine.asset_valuation import assess_asset_valuation
from app.engine.evidence import build_adjustment_evidence


REFERENCE_CODE = "1.02.03.01.06"


def test_existing_plra_discount_policy_calculates_default_value() -> None:
    assessment = _assess()

    assert assessment.default_desagio_percent == Decimal("0.800000")
    assert assessment.default_economic_value == Decimal("200.00")
    assert assessment.final_economic_value == Decimal("200.00")
    assert assessment.final_value_source == ValuationValueSource.DEFAULT_POLICY
    assert assessment.blocks_plra is False


def test_validated_forced_liquidation_value_precedes_default() -> None:
    assessment = _assess(
        valuation_required=True,
        valuation_basis=ValuationBasis.ABNT_NBR_14653_REPORT,
        forced_liquidation_value=Decimal("450.00"),
        valuation_status=ValuationStatus.VALIDATED,
        evidence=_validated_evidence(),
    )

    assert assessment.default_economic_value == Decimal("200.00")
    assert assessment.final_economic_value == Decimal("450.00")
    assert (
        assessment.final_value_source
        == ValuationValueSource.FORCED_LIQUIDATION
    )
    assert assessment.evidence_id == "evidence-asset-1"
    assert assessment.blocks_plra is False


def test_forced_liquidation_without_validated_support_keeps_default_and_blocks() -> None:
    assessment = _assess(
        realizability_classification=(
            AssetRealizability.FORCED_LIQUIDATION_REQUIRES_REPORT
        ),
        valuation_required=True,
        valuation_basis=ValuationBasis.ABNT_NBR_14653_REPORT,
        forced_liquidation_value=Decimal("450.00"),
        valuation_status=ValuationStatus.PENDING,
        evidence=None,
    )

    assert assessment.final_economic_value == Decimal("200.00")
    assert assessment.final_value_source == ValuationValueSource.DEFAULT_POLICY
    assert assessment.blocks_plra is True
    assert (
        "LIQUIDACAO_FORCADA_SEM_VALIDACAO_DOCUMENTAL"
        in assessment.blocking_reasons
    )
    assert "ATIVO_MATERIAL_SEM_LAUDO_VALIDADO" in assessment.blocking_reasons


def test_validated_manual_value_requires_evidence_and_justification() -> None:
    assessment = _assess(
        valuation_basis=ValuationBasis.ANALYST_ESTIMATE,
        analyst_adjusted_value=Decimal("325.00"),
        valuation_status=ValuationStatus.VALIDATED,
        evidence=_validated_evidence(),
    )

    assert assessment.final_economic_value == Decimal("325.00")
    assert (
        assessment.final_value_source
        == ValuationValueSource.ANALYST_ADJUSTMENT
    )
    assert assessment.blocks_plra is False


def test_manual_value_without_evidence_does_not_replace_default() -> None:
    assessment = _assess(
        valuation_basis=ValuationBasis.ANALYST_ESTIMATE,
        analyst_adjusted_value=Decimal("325.00"),
        valuation_status=ValuationStatus.VALIDATED,
        evidence=None,
    )

    assert assessment.final_economic_value == Decimal("200.00")
    assert assessment.blocks_plra is True
    assert (
        "VALOR_MANUAL_SEM_JUSTIFICATIVA_E_EVIDENCIA_VALIDADA"
        in assessment.blocking_reasons
    )


def test_asset_without_realizability_goes_to_zero() -> None:
    assessment = _assess(
        realizability_classification=AssetRealizability.NO_REALIZABILITY,
        valuation_basis=ValuationBasis.INTERNAL_POLICY,
    )

    assert assessment.final_economic_value == Decimal("0.00")
    assert (
        assessment.final_value_source
        == ValuationValueSource.ZERO_REALIZABILITY
    )
    assert assessment.valuation_basis == ValuationBasis.NOT_APPLICABLE
    assert assessment.blocks_plra is False


def test_essential_asset_is_not_automatically_zeroed() -> None:
    assessment = _assess(
        realizability_classification=AssetRealizability.NO_REALIZABILITY,
        essentiality_status=EssentialityStatus.ESSENTIAL,
    )

    assert assessment.final_economic_value == Decimal("200.00")
    assert assessment.final_value_source == ValuationValueSource.DEFAULT_POLICY
    assert assessment.blocks_plra is True
    assert (
        "ATIVO_ESSENCIAL_SEM_REALIZABILIDADE_EXIGE_REVISAO"
        in assessment.blocking_reasons
    )


def test_float_asset_value_is_rejected() -> None:
    with pytest.raises(TypeError, match="book_value must be Decimal"):
        _assess(book_value=1000.0)  # type: ignore[arg-type]


def test_snapshot_preserves_audit_values_as_decimal_strings() -> None:
    snapshot = _assess().to_snapshot()

    assert snapshot["book_value"] == "1000.00"
    assert snapshot["default_desagio_percent"] == "0.800000"
    assert snapshot["default_economic_value"] == "200.00"
    assert snapshot["final_economic_value"] == "200.00"
    assert snapshot["final_value_source"] == "politica_default"


def _assess(**overrides):
    values = {
        "assessment_id": "asset-assessment-1",
        "exercise_year": 2024,
        "account_code": "1.2.3",
        "account_name": "Maquinas e equipamentos",
        "reference_code": REFERENCE_CODE,
        "book_value": Decimal("1000.00"),
        "policy": load_plra_policy(),
        "realizability_classification": AssetRealizability.LONG_TERM,
        "valuation_required": False,
        "valuation_basis": ValuationBasis.INTERNAL_POLICY,
        "forced_liquidation_value": None,
        "analyst_adjusted_value": None,
        "essentiality_status": EssentialityStatus.NOT_ESSENTIAL,
        "valuation_status": ValuationStatus.NOT_REQUIRED,
        "evidence": None,
    }
    values.update(overrides)
    return assess_asset_valuation(**values)


def _validated_evidence():
    return build_adjustment_evidence(
        evidence_id="evidence-asset-1",
        exercise_year=2024,
        scope_type=EvidenceScopeType.ASSET_VALUATION,
        scope_key="1.2.3",
        adjustment_type="avaliacao_ativo",
        method_component=MethodComponent.PLRA,
        amount_impact=Decimal("125.00"),
        impact_base_value=Decimal("1000.00"),
        required_evidence_type="laudo_abnt_nbr_14653",
        evidence_status=EvidenceStatus.VALIDATED,
        analyst_justification="Valor suportado pela avaliacao apresentada.",
        review_notes=None,
        methodology_version_id="metodologia-2024.1",
        created_at=datetime(2026, 7, 24, tzinfo=timezone.utc),
    )

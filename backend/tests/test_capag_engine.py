from decimal import Decimal

import pytest

from app.domain import CapagEMethod, CapagEStatus, ComponentStatus
from app.engine import calculate_capag_e_assessment, map_plr_ajustado_to_plra


def test_fca_plra_calculates_final_assessment() -> None:
    assessment = _calculate(
        method=CapagEMethod.FCA_PLRA,
        fca_value=Decimal("120000.00"),
        fca_status=ComponentStatus.CALCULATED,
    )

    assert assessment.capag_e_value == Decimal("620000.00")
    assert assessment.capag_e_status == CapagEStatus.CALCULATED
    assert assessment.methodology_formula == "CAPAG-E = PLRA + FCA"


def test_roa_plra_calculates_final_assessment() -> None:
    assessment = _calculate(
        method=CapagEMethod.ROA_PLRA,
        roa_value=Decimal("80000.00"),
        roa_status=ComponentStatus.CALCULATED,
    )

    assert assessment.capag_e_value == Decimal("580000.00")
    assert assessment.capag_e_status == CapagEStatus.CALCULATED
    assert assessment.methodology_formula == "CAPAG-E = PLRA + ROA"


def test_missing_plra_blocks_assessment_and_preserves_fca() -> None:
    assessment = _calculate(
        method=CapagEMethod.FCA_PLRA,
        plra_value=None,
        plra_status=ComponentStatus.BLOCKED_BY_PENDING,
        fca_value=Decimal("120000.00"),
        fca_status=ComponentStatus.CALCULATED,
    )

    assert assessment.capag_e_value is None
    assert assessment.capag_e_status == CapagEStatus.BLOCKED
    assert assessment.fca_value == Decimal("120000.00")
    assert "PLRA_FINAL_INDISPONIVEL" in assessment.blocking_issues


@pytest.mark.parametrize(
    ("method", "component_name"),
    [
        (CapagEMethod.FCA_PLRA, "FCA"),
        (CapagEMethod.ROA_PLRA, "ROA"),
    ],
)
def test_selected_method_without_final_component_is_blocked(
    method: CapagEMethod,
    component_name: str,
) -> None:
    assessment = _calculate(method=method)

    assert assessment.capag_e_value is None
    assert assessment.capag_e_status == CapagEStatus.BLOCKED
    assert f"{component_name}_FINAL_INDISPONIVEL" in assessment.blocking_issues


def test_fco_is_exposed_as_partial_fca_and_never_as_final() -> None:
    assessment = _calculate(
        method=CapagEMethod.FCA_PLRA,
        fco_value=Decimal("40000.00"),
    )

    assert assessment.fca_value == Decimal("40000.00")
    assert assessment.fca_status == ComponentStatus.PARTIAL
    assert assessment.capag_e_value == Decimal("540000.00")
    assert assessment.capag_e_status == CapagEStatus.PARTIAL
    assert any("FCA parcial" in item for item in assessment.limitations)


def test_undefined_method_blocks_final_result() -> None:
    assessment = _calculate(
        method=CapagEMethod.UNDEFINED,
        fca_value=Decimal("120000.00"),
        fca_status=ComponentStatus.CALCULATED,
    )

    assert assessment.capag_e_status == CapagEStatus.BLOCKED
    assert assessment.capag_e_value is None
    assert "METODO_CAPAG_E_NAO_DEFINIDO" in assessment.blocking_issues


def test_comparison_preserves_both_paths_and_reports_divergence() -> None:
    assessment = _calculate(
        method=CapagEMethod.COMPARATIVO_FCA_ROA,
        fca_value=Decimal("120000.00"),
        fca_status=ComponentStatus.CALCULATED,
        roa_value=Decimal("80000.00"),
        roa_status=ComponentStatus.CALCULATED,
    )

    assert assessment.capag_e_value is None
    assert assessment.capag_e_status == CapagEStatus.PARTIAL
    assert "PLRA+FCA=620000.00" in assessment.calculation_basis
    assert "PLRA+ROA=580000.00" in assessment.calculation_basis
    assert assessment.warnings == (
        "Divergencia entre os caminhos PLRA + FCA e PLRA + ROA.",
    )


def test_plr_ajustado_maps_to_canonical_plra() -> None:
    assert map_plr_ajustado_to_plra(Decimal("100.005")) == Decimal("100.00")


def test_engine_rejects_float_before_calculation() -> None:
    with pytest.raises(TypeError, match="plra_value must be Decimal or None"):
        _calculate(
            method=CapagEMethod.FCA_PLRA,
            plra_value=500000.0,
            fca_value=Decimal("120000.00"),
            fca_status=ComponentStatus.CALCULATED,
        )


def _calculate(**overrides: object):
    values = {
        "exercise_year": 2024,
        "method": CapagEMethod.FCA_PLRA,
        "plra_value": Decimal("500000.00"),
        "plra_status": ComponentStatus.CALCULATED,
        "methodology_version_id": "metodologia-2024.1",
    }
    values.update(overrides)
    return calculate_capag_e_assessment(**values)

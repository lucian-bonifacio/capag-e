from decimal import Decimal

import pytest

from app.domain import (
    CapagEAssessment,
    CapagEMethod,
    CapagEStatus,
    ComponentStatus,
)


def test_capag_assessment_quantizes_values_and_serializes_canonical_contract() -> None:
    assessment = _assessment(
        plra_value=Decimal("500000.005"),
        fca_value=Decimal("120000.004"),
        capag_e_value=Decimal("620000.009"),
    )

    assert assessment.plra_value == Decimal("500000.00")
    assert assessment.fca_value == Decimal("120000.00")
    assert assessment.capag_e_value == Decimal("620000.01")
    assert assessment.to_snapshot()["capag_e_value"] == "620000.01"
    assert assessment.to_snapshot()["method"] == "fca_plra"


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("method", "metodo_inexistente"),
        ("plra_status", "status_inexistente"),
        ("capag_e_status", "final"),
    ],
)
def test_capag_assessment_rejects_invalid_methods_and_statuses(
    field_name: str,
    invalid_value: str,
) -> None:
    values = _assessment_values()
    values[field_name] = invalid_value

    with pytest.raises(ValueError, match=f"invalid {field_name}"):
        CapagEAssessment(**values)


@pytest.mark.parametrize(
    "field_name",
    ["plra_value", "fca_value", "roa_value", "capag_e_value"],
)
def test_capag_assessment_rejects_float_values(field_name: str) -> None:
    values = _assessment_values()
    values[field_name] = 1.5
    if field_name == "roa_value":
        values["roa_status"] = ComponentStatus.CALCULATED

    with pytest.raises(TypeError, match=f"{field_name} must be Decimal or None"):
        CapagEAssessment(**values)


def test_calculated_component_requires_value() -> None:
    values = _assessment_values()
    values["fca_value"] = None

    with pytest.raises(
        ValueError,
        match="fca_value is required when fca_status is calculado",
    ):
        CapagEAssessment(**values)


def _assessment(**overrides: object) -> CapagEAssessment:
    values = _assessment_values()
    values.update(overrides)
    return CapagEAssessment(**values)


def _assessment_values() -> dict[str, object]:
    return {
        "exercise_year": 2024,
        "method": CapagEMethod.FCA_PLRA,
        "plra_value": Decimal("500000.00"),
        "plra_status": ComponentStatus.CALCULATED,
        "fca_value": Decimal("120000.00"),
        "fca_status": ComponentStatus.CALCULATED,
        "roa_value": None,
        "roa_status": ComponentStatus.NOT_CALCULATED,
        "capag_e_value": Decimal("620000.00"),
        "capag_e_status": CapagEStatus.CALCULATED,
        "unavailable_reason": None,
        "calculation_basis": "PLRA=500000.00; FCA=120000.00",
        "methodology_formula": "CAPAG-E = PLRA + FCA",
        "warnings": (),
        "limitations": (),
        "blocking_issues": (),
        "methodology_version_id": "metodologia-2024.1",
    }

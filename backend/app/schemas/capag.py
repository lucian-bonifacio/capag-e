from __future__ import annotations

from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.application.capag_service import CapagAssessmentRunInput
from app.domain import (
    CapagEAssessment,
    CapagEMethod,
    CapagEStatus,
    ComponentStatus,
)


class CapagAssessmentRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method: CapagEMethod
    fca_value: str | None = None
    fca_status: ComponentStatus = ComponentStatus.NOT_CALCULATED
    roa_value: str | None = None
    roa_status: ComponentStatus = ComponentStatus.NOT_CALCULATED
    fco_value: str | None = None
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    blocking_issues: list[str] = Field(default_factory=list)

    @field_validator("fca_value", "roa_value", "fco_value")
    @classmethod
    def validate_decimal_string(cls, value: str | None) -> str | None:
        if value is None:
            return None
        try:
            parsed = Decimal(value)
        except InvalidOperation as exc:
            raise ValueError("value must be a decimal string") from exc
        if not parsed.is_finite():
            raise ValueError("value must be a finite decimal string")
        return value

    def to_run_input(self) -> CapagAssessmentRunInput:
        return CapagAssessmentRunInput(
            method=self.method,
            fca_value=_to_decimal(self.fca_value),
            fca_status=self.fca_status,
            roa_value=_to_decimal(self.roa_value),
            roa_status=self.roa_status,
            fco_value=_to_decimal(self.fco_value),
            warnings=tuple(self.warnings),
            limitations=tuple(self.limitations),
            blocking_issues=tuple(self.blocking_issues),
        )


class CapagAssessmentResponse(BaseModel):
    exercise_year: int
    method: CapagEMethod
    plra_value: str | None
    plra_status: ComponentStatus
    fca_value: str | None
    fca_status: ComponentStatus
    roa_value: str | None
    roa_status: ComponentStatus
    capag_e_value: str | None
    capag_e_status: CapagEStatus
    unavailable_reason: str | None
    calculation_basis: str
    methodology_formula: str
    warnings: list[str]
    limitations: list[str]
    blocking_issues: list[str]
    methodology_version_id: str

    @classmethod
    def from_domain(cls, assessment: CapagEAssessment) -> "CapagAssessmentResponse":
        return cls(
            exercise_year=assessment.exercise_year,
            method=assessment.method,
            plra_value=_format_decimal(assessment.plra_value),
            plra_status=assessment.plra_status,
            fca_value=_format_decimal(assessment.fca_value),
            fca_status=assessment.fca_status,
            roa_value=_format_decimal(assessment.roa_value),
            roa_status=assessment.roa_status,
            capag_e_value=_format_decimal(assessment.capag_e_value),
            capag_e_status=assessment.capag_e_status,
            unavailable_reason=assessment.unavailable_reason,
            calculation_basis=assessment.calculation_basis,
            methodology_formula=assessment.methodology_formula,
            warnings=list(assessment.warnings),
            limitations=list(assessment.limitations),
            blocking_issues=list(assessment.blocking_issues),
            methodology_version_id=assessment.methodology_version_id,
        )


class CapagApiErrorResponse(BaseModel):
    error_code: str
    message: str


def _to_decimal(value: str | None) -> Decimal | None:
    if value is None:
        return None
    return Decimal(value)


def _format_decimal(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return format(value, "f")

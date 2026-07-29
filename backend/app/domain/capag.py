from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Any, TypeVar

from app.domain.declared_balance import DeclaredBalanceStatus


CENT = Decimal("0.01")


class CapagEMethod(StrEnum):
    FCA_PLRA = "fca_plra"
    ROA_PLRA = "roa_plra"
    COMPARATIVO_FCA_ROA = "comparativo_fca_roa"
    UNDEFINED = "nao_definido"


class ComponentStatus(StrEnum):
    NOT_CALCULATED = "nao_calculado"
    CALCULATED = "calculado"
    PARTIAL = "parcial"
    BLOCKED_BY_PENDING = "bloqueado_por_pendencia"
    BLOCKED_BY_EVIDENCE = "bloqueado_por_evidencia"
    METHODOLOGY_ERROR = "erro_metodologico"


class CapagEStatus(StrEnum):
    NOT_CALCULATED = "nao_calculado"
    PARTIAL = "parcial"
    CALCULATED = "calculado"
    BLOCKED = "bloqueado"
    UNAVAILABLE = "indisponivel"
    METHODOLOGY_ERROR = "erro_metodologico"


@dataclass(frozen=True)
class CapagEAssessment:
    exercise_year: int
    method: CapagEMethod
    plra_value: Decimal | None
    plra_status: ComponentStatus
    fca_value: Decimal | None
    fca_status: ComponentStatus
    roa_value: Decimal | None
    roa_status: ComponentStatus
    capag_e_value: Decimal | None
    capag_e_status: CapagEStatus
    unavailable_reason: str | None
    calculation_basis: str
    methodology_formula: str
    warnings: tuple[str, ...]
    limitations: tuple[str, ...]
    blocking_issues: tuple[str, ...]
    methodology_version_id: str
    balance_status: DeclaredBalanceStatus = DeclaredBalanceStatus.VALIDO

    def __post_init__(self) -> None:
        if isinstance(self.exercise_year, bool) or not isinstance(self.exercise_year, int):
            raise TypeError("exercise_year must be int")
        if self.exercise_year < 1:
            raise ValueError("exercise_year must be positive")

        object.__setattr__(
            self,
            "method",
            _coerce_enum("method", self.method, CapagEMethod),
        )
        for field_name in ("plra_status", "fca_status", "roa_status"):
            object.__setattr__(
                self,
                field_name,
                _coerce_enum(field_name, getattr(self, field_name), ComponentStatus),
            )
        object.__setattr__(
            self,
            "capag_e_status",
            _coerce_enum("capag_e_status", self.capag_e_status, CapagEStatus),
        )
        object.__setattr__(
            self,
            "balance_status",
            _coerce_enum(
                "balance_status",
                self.balance_status,
                DeclaredBalanceStatus,
            ),
        )

        for field_name in ("plra_value", "fca_value", "roa_value", "capag_e_value"):
            object.__setattr__(
                self,
                field_name,
                _quantize_optional_decimal(field_name, getattr(self, field_name)),
            )

        for field_name in ("warnings", "limitations", "blocking_issues"):
            object.__setattr__(
                self,
                field_name,
                _normalize_messages(field_name, getattr(self, field_name)),
            )

        if not self.calculation_basis.strip():
            raise ValueError("calculation_basis is required")
        if not self.methodology_formula.strip():
            raise ValueError("methodology_formula is required")
        if not self.methodology_version_id.strip():
            raise ValueError("methodology_version_id is required")

        _validate_component_value("plra", self.plra_value, self.plra_status)
        _validate_component_value("fca", self.fca_value, self.fca_status)
        _validate_component_value("roa", self.roa_value, self.roa_status)
        if self.capag_e_status == CapagEStatus.CALCULATED and self.capag_e_value is None:
            raise ValueError("capag_e_value is required when capag_e_status is calculado")

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "exercise_year": self.exercise_year,
            "method": self.method.value,
            "plra_value": _decimal_to_string(self.plra_value),
            "plra_status": self.plra_status.value,
            "fca_value": _decimal_to_string(self.fca_value),
            "fca_status": self.fca_status.value,
            "roa_value": _decimal_to_string(self.roa_value),
            "roa_status": self.roa_status.value,
            "capag_e_value": _decimal_to_string(self.capag_e_value),
            "capag_e_status": self.capag_e_status.value,
            "unavailable_reason": self.unavailable_reason,
            "calculation_basis": self.calculation_basis,
            "methodology_formula": self.methodology_formula,
            "warnings": list(self.warnings),
            "limitations": list(self.limitations),
            "blocking_issues": list(self.blocking_issues),
            "methodology_version_id": self.methodology_version_id,
            "balance_status": self.balance_status.value,
        }


EnumT = TypeVar("EnumT", bound=StrEnum)


def _coerce_enum(field_name: str, value: object, enum_type: type[EnumT]) -> EnumT:
    if isinstance(value, enum_type):
        return value
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid {field_name}: {value}") from exc


def _quantize_optional_decimal(field_name: str, value: object) -> Decimal | None:
    if value is None:
        return None
    if not isinstance(value, Decimal):
        raise TypeError(f"{field_name} must be Decimal or None")
    if not value.is_finite():
        raise ValueError(f"{field_name} must be finite")
    return value.quantize(CENT)


def _normalize_messages(field_name: str, values: object) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        raise TypeError(f"{field_name} must be a list or tuple of strings")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError(f"{field_name} must contain non-empty strings")
    return tuple(values)


def _validate_component_value(
    component_name: str,
    value: Decimal | None,
    status: ComponentStatus,
) -> None:
    if status in {ComponentStatus.CALCULATED, ComponentStatus.PARTIAL} and value is None:
        raise ValueError(
            f"{component_name}_value is required when {component_name}_status is {status.value}"
        )
    if status == ComponentStatus.NOT_CALCULATED and value is not None:
        raise ValueError(
            f"{component_name}_value must be None when "
            f"{component_name}_status is nao_calculado"
        )


def _decimal_to_string(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return format(value, "f")

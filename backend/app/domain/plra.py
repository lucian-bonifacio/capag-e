from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from app.domain.capag import CENT, ComponentStatus
from app.domain.declared_balance import DeclaredBalanceStatus


class PlraInclusionStatus(StrEnum):
    INCLUDED_ASSET = "incluido_ativo"
    INCLUDED_LIABILITY = "incluido_passivo"
    EXCLUDED = "excluido"
    PENDING = "pendente"
    IGNORED_HIERARCHY = "ignorado_hierarquia"
    NO_REFERENCE = "sem_vinculo_referencial"
    NON_PATRIMONIAL = "nao_patrimonial"


class PlraDecisionStatus(StrEnum):
    AUTOMATIC = "automatica"
    VALIDATED = "validada"
    PENDING = "pendente"
    NOT_APPLICABLE = "nao_aplicavel"


@dataclass(frozen=True)
class PlraAccountInput:
    account_code: str
    account_name: str
    account_type: str | None
    account_level: int | None
    parent_account_code: str | None
    declared_reference_code: str | None
    official_description: str | None
    official_nature: str | None
    final_balance: Decimal
    final_balance_indicator: str

    def __post_init__(self) -> None:
        if not self.account_code.strip() or not self.account_name.strip():
            raise ValueError("PLRA account code and name are required.")
        if not isinstance(self.final_balance, Decimal):
            raise TypeError("PLRA final_balance must be Decimal.")
        if not self.final_balance.is_finite():
            raise ValueError("PLRA final_balance must be finite.")
        if self.final_balance_indicator not in {"D", "C"}:
            raise ValueError("PLRA final_balance_indicator must be D or C.")


@dataclass(frozen=True)
class PlraAccountAuditRow:
    account_code: str
    account_name: str
    account_type: str | None
    account_level: int | None
    parent_account_code: str | None
    declared_reference_code: str | None
    official_description: str | None
    methodology_rule_id: str | None
    methodology_group: str | None
    macrogroup: str | None
    base_value: Decimal
    sign: str
    inclusion_status: PlraInclusionStatus
    default_discount_percent: Decimal | None
    default_economic_value: Decimal
    valuation_source: str | None
    validated_valuation_value: Decimal | None
    final_economic_value: Decimal
    decision_status: PlraDecisionStatus
    evidence_status: str | None
    reason: str
    limitations: tuple[str, ...]
    methodology_version_id: str

    def __post_init__(self) -> None:
        for field in {
            "base_value",
            "default_economic_value",
            "validated_valuation_value",
            "final_economic_value",
        }:
            value = getattr(self, field)
            if value is not None:
                object.__setattr__(self, field, _money(field, value))
        if self.default_discount_percent is not None:
            value = self.default_discount_percent
            if not isinstance(value, Decimal):
                raise TypeError("default_discount_percent must be Decimal or None.")
            if value < Decimal("0") or value > Decimal("1"):
                raise ValueError("default_discount_percent must be between zero and one.")
        object.__setattr__(
            self,
            "inclusion_status",
            PlraInclusionStatus(self.inclusion_status),
        )
        object.__setattr__(
            self,
            "decision_status",
            PlraDecisionStatus(self.decision_status),
        )
        object.__setattr__(self, "limitations", tuple(self.limitations))
        if not self.reason.strip() or not self.methodology_version_id.strip():
            raise ValueError("PLRA audit reason and methodology version are required.")

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "account_code": self.account_code,
            "account_name": self.account_name,
            "account_type": self.account_type,
            "account_level": self.account_level,
            "parent_account_code": self.parent_account_code,
            "declared_reference_code": self.declared_reference_code,
            "official_description": self.official_description,
            "methodology_rule_id": self.methodology_rule_id,
            "methodology_group": self.methodology_group,
            "macrogroup": self.macrogroup,
            "base_value": format(self.base_value, "f"),
            "sign": self.sign,
            "inclusion_status": self.inclusion_status.value,
            "default_discount_percent": _decimal_string(
                self.default_discount_percent
            ),
            "default_economic_value": format(self.default_economic_value, "f"),
            "valuation_source": self.valuation_source,
            "validated_valuation_value": _decimal_string(
                self.validated_valuation_value
            ),
            "final_economic_value": format(self.final_economic_value, "f"),
            "decision_status": self.decision_status.value,
            "evidence_status": self.evidence_status,
            "reason": self.reason,
            "limitations": list(self.limitations),
            "methodology_version_id": self.methodology_version_id,
        }


@dataclass(frozen=True)
class PlraCalculation:
    analysis_id: str
    exercise_year: int
    gross_assets_value: Decimal
    gross_economic_liabilities_value: Decimal
    adjusted_assets_value: Decimal
    plr_gross_value: Decimal
    plra_value: Decimal
    plra_status: ComponentStatus
    calculation_formula: str
    account_rows: tuple[PlraAccountAuditRow, ...]
    pending_accounts: tuple[str, ...]
    warnings: tuple[str, ...]
    limitations: tuple[str, ...]
    blocking_issues: tuple[str, ...]
    methodology_version_id: str
    calculated_at: datetime
    balance_status: DeclaredBalanceStatus = DeclaredBalanceStatus.VALIDO

    def __post_init__(self) -> None:
        for field in {
            "gross_assets_value",
            "gross_economic_liabilities_value",
            "adjusted_assets_value",
            "plr_gross_value",
            "plra_value",
        }:
            object.__setattr__(self, field, _money(field, getattr(self, field)))
        object.__setattr__(self, "plra_status", ComponentStatus(self.plra_status))
        object.__setattr__(
            self,
            "balance_status",
            DeclaredBalanceStatus(self.balance_status),
        )
        for field in {
            "account_rows",
            "pending_accounts",
            "warnings",
            "limitations",
            "blocking_issues",
        }:
            object.__setattr__(self, field, tuple(getattr(self, field)))
        if not self.analysis_id.strip() or self.exercise_year < 1:
            raise ValueError("PLRA analysis and exercise are required.")
        if not self.methodology_version_id.strip():
            raise ValueError("PLRA methodology_version_id is required.")

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "analysis_id": self.analysis_id,
            "exercise_year": self.exercise_year,
            "gross_assets_value": format(self.gross_assets_value, "f"),
            "gross_economic_liabilities_value": format(
                self.gross_economic_liabilities_value, "f"
            ),
            "adjusted_assets_value": format(self.adjusted_assets_value, "f"),
            "plr_gross_value": format(self.plr_gross_value, "f"),
            "plra_value": format(self.plra_value, "f"),
            "plra_status": self.plra_status.value,
            "calculation_formula": self.calculation_formula,
            "account_rows": [row.to_snapshot() for row in self.account_rows],
            "pending_accounts": list(self.pending_accounts),
            "warnings": list(self.warnings),
            "limitations": list(self.limitations),
            "blocking_issues": list(self.blocking_issues),
            "balance_status": self.balance_status.value,
            "methodology_version_id": self.methodology_version_id,
            "calculated_at": self.calculated_at.isoformat(),
        }


def _money(field: str, value: object) -> Decimal:
    if not isinstance(value, Decimal):
        raise TypeError(f"{field} must be Decimal.")
    if not value.is_finite():
        raise ValueError(f"{field} must be finite.")
    return value.quantize(CENT)


def _decimal_string(value: Decimal | None) -> str | None:
    return None if value is None else format(value, "f")

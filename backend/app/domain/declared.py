from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from app.engine.methodology_matcher import MatchResult


@dataclass(frozen=True)
class DeclaredAccountResult:
    account_code: str
    account_name: str
    declared_reference_code: str | None
    official_description: str | None
    official_reference_status: str | None
    methodology_rule_applied: str | None
    methodology_rule_status: str | None
    purpose: str
    plra_category: str | None
    fco_category: str | None
    capag_category: str | None
    flow_nature: str | None
    treatment: str | None
    base_value: Decimal
    considered_value: Decimal
    final_status: str
    observation: str | None
    recommended_action: str | None
    methodology_version_id: str

    @classmethod
    def from_match(
        cls,
        *,
        account_code: str,
        account_name: str,
        declared_reference_code: str | None,
        purpose: str,
        base_value: Decimal,
        considered_value: Decimal,
        methodology_version_id: str,
        match_result: MatchResult,
    ) -> "DeclaredAccountResult":
        _require_decimal("base_value", base_value)
        _require_decimal("considered_value", considered_value)

        methodology_rule = match_result.methodology_rule
        official_reference = match_result.official_reference

        return cls(
            account_code=account_code,
            account_name=account_name,
            declared_reference_code=declared_reference_code,
            official_description=(
                official_reference.official_description if official_reference is not None else None
            ),
            official_reference_status=(
                official_reference.status if official_reference is not None else match_result.final_status.value
            ),
            methodology_rule_applied=match_result.methodology_rule_applied,
            methodology_rule_status=(
                match_result.methodology_rule_status.value
                if match_result.methodology_rule_status is not None
                else None
            ),
            purpose=purpose,
            plra_category=methodology_rule.plra_category if methodology_rule is not None else None,
            fco_category=methodology_rule.fco_category if methodology_rule is not None else None,
            capag_category=methodology_rule.capag_category if methodology_rule is not None else None,
            flow_nature=methodology_rule.flow_nature if methodology_rule is not None else None,
            treatment=methodology_rule.operational_treatment if methodology_rule is not None else None,
            base_value=base_value,
            considered_value=considered_value,
            final_status=match_result.final_status.value,
            observation=match_result.observation,
            recommended_action=match_result.recommended_action,
            methodology_version_id=methodology_version_id,
        )

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "account_code": self.account_code,
            "account_name": self.account_name,
            "declared_reference_code": self.declared_reference_code,
            "official_description": self.official_description,
            "official_reference_status": self.official_reference_status,
            "methodology_rule_applied": self.methodology_rule_applied,
            "methodology_rule_status": self.methodology_rule_status,
            "purpose": self.purpose,
            "plra_category": self.plra_category,
            "fco_category": self.fco_category,
            "capag_category": self.capag_category,
            "flow_nature": self.flow_nature,
            "treatment": self.treatment,
            "base_value": _decimal_to_string(self.base_value),
            "considered_value": _decimal_to_string(self.considered_value),
            "final_status": self.final_status,
            "observation": self.observation,
            "recommended_action": self.recommended_action,
            "methodology_version_id": self.methodology_version_id,
        }


def _require_decimal(field_name: str, value: Decimal) -> None:
    if not isinstance(value, Decimal):
        raise TypeError(f"{field_name} must be Decimal")


def _decimal_to_string(value: Decimal) -> str:
    return format(value, "f")


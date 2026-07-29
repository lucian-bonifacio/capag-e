from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.domain import (
    ComponentStatus,
    PlraAccountAuditRow,
    PlraCalculation,
    PlraDecisionStatus,
    PlraInclusionStatus,
)


class PlraCalculationResponse(BaseModel):
    analysis_id: str
    exercise_year: int
    gross_assets_value: str
    gross_economic_liabilities_value: str
    adjusted_assets_value: str
    plr_gross_value: str
    plra_value: str
    plra_status: ComponentStatus
    calculation_formula: str
    pending_accounts: list[str]
    warnings: list[str]
    limitations: list[str]
    blocking_issues: list[str]
    balance_status: str
    methodology_version_id: str
    calculated_at: datetime

    @classmethod
    def from_domain(cls, calculation: PlraCalculation) -> "PlraCalculationResponse":
        return cls(
            analysis_id=calculation.analysis_id,
            exercise_year=calculation.exercise_year,
            gross_assets_value=_decimal_string(calculation.gross_assets_value),
            gross_economic_liabilities_value=_decimal_string(
                calculation.gross_economic_liabilities_value
            ),
            adjusted_assets_value=_decimal_string(calculation.adjusted_assets_value),
            plr_gross_value=_decimal_string(calculation.plr_gross_value),
            plra_value=_decimal_string(calculation.plra_value),
            plra_status=calculation.plra_status,
            calculation_formula=calculation.calculation_formula,
            pending_accounts=list(calculation.pending_accounts),
            warnings=list(calculation.warnings),
            limitations=list(calculation.limitations),
            blocking_issues=list(calculation.blocking_issues),
            balance_status=calculation.balance_status.value,
            methodology_version_id=calculation.methodology_version_id,
            calculated_at=calculation.calculated_at,
        )


class PlraAccountAuditRowResponse(BaseModel):
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
    base_value: str
    sign: str
    inclusion_status: PlraInclusionStatus
    default_discount_percent: str | None
    default_economic_value: str
    valuation_source: str | None
    validated_valuation_value: str | None
    final_economic_value: str
    decision_status: PlraDecisionStatus
    evidence_status: str | None
    reason: str
    limitations: list[str]
    methodology_version_id: str

    @classmethod
    def from_domain(cls, row: PlraAccountAuditRow) -> "PlraAccountAuditRowResponse":
        return cls(
            account_code=row.account_code,
            account_name=row.account_name,
            account_type=row.account_type,
            account_level=row.account_level,
            parent_account_code=row.parent_account_code,
            declared_reference_code=row.declared_reference_code,
            official_description=row.official_description,
            methodology_rule_id=row.methodology_rule_id,
            methodology_group=row.methodology_group,
            macrogroup=row.macrogroup,
            base_value=_decimal_string(row.base_value),
            sign=row.sign,
            inclusion_status=row.inclusion_status,
            default_discount_percent=_optional_decimal_string(
                row.default_discount_percent
            ),
            default_economic_value=_decimal_string(row.default_economic_value),
            valuation_source=row.valuation_source,
            validated_valuation_value=_optional_decimal_string(
                row.validated_valuation_value
            ),
            final_economic_value=_decimal_string(row.final_economic_value),
            decision_status=row.decision_status,
            evidence_status=row.evidence_status,
            reason=row.reason,
            limitations=list(row.limitations),
            methodology_version_id=row.methodology_version_id,
        )


class PlraAuditResponse(BaseModel):
    analysis_id: str
    exercise_year: int
    plra_status: ComponentStatus
    methodology_version_id: str
    rows: list[PlraAccountAuditRowResponse]

    @classmethod
    def from_domain(cls, calculation: PlraCalculation) -> "PlraAuditResponse":
        return cls(
            analysis_id=calculation.analysis_id,
            exercise_year=calculation.exercise_year,
            plra_status=calculation.plra_status,
            methodology_version_id=calculation.methodology_version_id,
            rows=[
                PlraAccountAuditRowResponse.from_domain(row)
                for row in calculation.account_rows
            ],
        )


class PlraApiErrorResponse(BaseModel):
    error_code: str
    message: str


def _decimal_string(value: Decimal) -> str:
    return format(value, "f")


def _optional_decimal_string(value: Decimal | None) -> str | None:
    return None if value is None else _decimal_string(value)

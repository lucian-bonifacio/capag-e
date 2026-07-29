from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_serializer


class DeclaredAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_code: str
    account_name: str
    account_type: str | None
    account_nature: str | None
    account_level: int | None
    parent_account_code: str | None
    account_order: int | None
    declared_reference_code: str | None
    official_description: str | None
    official_reference_status: str | None
    methodology_rule_applied: str | None
    methodology_rule_status: str | None
    purpose: str
    treatment: str | None
    base_value: Decimal
    considered_value: Decimal
    final_status: str
    observation: str | None
    recommended_action: str | None
    methodology_version_id: str

    @field_serializer("base_value", "considered_value")
    def serialize_decimal(self, value: Decimal) -> str:
        return format(value, "f")


class DeclaredAccountsResponse(BaseModel):
    analysis_id: str
    year: int
    accounts: list[DeclaredAccountResponse]


class DeclaredBalanceRowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    aggregation_code: str
    aggregation_code_type: str
    aggregation_level: int
    parent_aggregation_code: str | None
    balance_group: str
    description: str
    initial_amount: Decimal
    initial_debit_credit_indicator: str
    final_amount: Decimal
    final_debit_credit_indicator: str
    explanatory_note_reference: str | None
    line_number: int
    structural_status: str
    reconciliation_status: str | None
    reconciled_amount: Decimal | None
    difference: Decimal | None
    component_count: int
    children: list["DeclaredBalanceRowResponse"]

    @field_serializer(
        "initial_amount",
        "final_amount",
        "reconciled_amount",
        "difference",
    )
    def serialize_money(self, value: Decimal | None) -> str | None:
        return format(value, "f") if value is not None else None


class DeclaredBalanceResponse(BaseModel):
    analysis_id: str
    year: int
    balance_status: str
    is_blocking: bool
    j005_period_start: date | None
    j005_period_end: date | None
    assets_final_amount: Decimal | None
    liabilities_and_equity_final_amount: Decimal | None
    difference: Decimal | None
    rows: list[DeclaredBalanceRowResponse]
    limitations: list[str]

    @field_serializer(
        "assets_final_amount",
        "liabilities_and_equity_final_amount",
        "difference",
    )
    def serialize_money(self, value: Decimal | None) -> str | None:
        return format(value, "f") if value is not None else None


class DeclaredBalanceComponentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_code: str
    account_name: str
    cost_center_code: str | None
    final_amount: Decimal | None
    final_debit_credit_indicator: str | None
    signed_final_amount: Decimal | None
    i052_line_number: int
    i155_line_number: int | None

    @field_serializer("final_amount", "signed_final_amount")
    def serialize_money(self, value: Decimal | None) -> str | None:
        return format(value, "f") if value is not None else None


class DeclaredBalanceComponentsResponse(BaseModel):
    analysis_id: str
    year: int
    aggregation_code: str
    rows: list[DeclaredBalanceComponentResponse]


class DeclaredLayerSummaryResponse(BaseModel):
    analysis_id: str
    year: int
    total_accounts: int
    status_counts: dict[str, int]
    methodology_version_id: str | None


class DeclaredRunResponse(BaseModel):
    analysis_id: str
    year: int
    status: str
    snapshots_created: int
    status_counts: dict[str, int]


class ApiErrorResponse(BaseModel):
    error_code: str
    message: str

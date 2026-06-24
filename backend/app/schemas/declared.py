from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_serializer


class DeclaredAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_code: str
    account_name: str
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


class DeclaredLayerSummaryResponse(BaseModel):
    analysis_id: str
    year: int
    total_accounts: int
    status_counts: dict[str, int]
    methodology_version_id: str | None


class ApiErrorResponse(BaseModel):
    error_code: str
    message: str


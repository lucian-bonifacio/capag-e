from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain import (
    CashFlowDirection,
    ComponentStatus,
    DfcActivity,
    DfcAuditRow,
    DfcCalculation,
    DfcComponentSummary,
    DfcDecisionAction,
    DfcPendingIssue,
    DfcRowStatus,
)


class DfcComponentSummaryResponse(BaseModel):
    activity: DfcActivity
    component_code: str
    component_label: str
    value: str
    movement_count: int

    @classmethod
    def from_domain(
        cls, summary: DfcComponentSummary
    ) -> "DfcComponentSummaryResponse":
        return cls(
            activity=summary.activity,
            component_code=summary.component_code,
            component_label=summary.component_label,
            value=format(summary.value, "f"),
            movement_count=summary.movement_count,
        )


class DfcAuditRowResponse(BaseModel):
    entry_number: str
    entry_date: date | None
    cash_account_code: str
    cash_flow_direction: CashFlowDirection
    counterparty_account_code: str
    counterparty_account_name: str
    counterparty_reference_code: str | None
    dfc_activity: DfcActivity
    dfc_component_code: str | None
    dfc_component_label: str | None
    movement_value: str
    included_value: str
    final_status: DfcRowStatus
    pending_reason: str | None
    history: str | None
    line_number: int

    @classmethod
    def from_domain(cls, row: DfcAuditRow) -> "DfcAuditRowResponse":
        return cls(
            entry_number=row.entry_number,
            entry_date=row.entry_date,
            cash_account_code=row.cash_account_code,
            cash_flow_direction=row.cash_flow_direction,
            counterparty_account_code=row.counterparty_account_code,
            counterparty_account_name=row.counterparty_account_name,
            counterparty_reference_code=row.counterparty_reference_code,
            dfc_activity=row.dfc_activity,
            dfc_component_code=row.dfc_component_code,
            dfc_component_label=row.dfc_component_label,
            movement_value=format(row.movement_value, "f"),
            included_value=format(row.included_value, "f"),
            final_status=row.final_status,
            pending_reason=row.pending_reason,
            history=row.history,
            line_number=row.line_number,
        )


class DfcPendingIssueResponse(BaseModel):
    code: str
    message: str
    entry_number: str | None
    line_number: int | None
    materiality_level: str | None
    blocks_fca: bool

    @classmethod
    def from_domain(cls, issue: DfcPendingIssue) -> "DfcPendingIssueResponse":
        return cls(**issue.to_snapshot())


class DfcCalculationResponse(BaseModel):
    exercise_year: int
    automatic_value: str
    operational_flow: str
    investment_flow: str
    financing_flow: str
    manual_adjustments_value: str
    fca_value: str
    fca_status: ComponentStatus
    component_summaries: list[DfcComponentSummaryResponse]
    audit_rows: list[DfcAuditRowResponse]
    pending_issues: list[DfcPendingIssueResponse]
    alerts: list[str]
    limitations: list[str]
    methodology_version_id: str

    @classmethod
    def from_domain(cls, calculation: DfcCalculation) -> "DfcCalculationResponse":
        return cls(
            exercise_year=calculation.exercise_year,
            automatic_value=format(calculation.automatic_value, "f"),
            operational_flow=format(calculation.operational_flow, "f"),
            investment_flow=format(calculation.investment_flow, "f"),
            financing_flow=format(calculation.financing_flow, "f"),
            manual_adjustments_value=format(
                calculation.manual_adjustments_value, "f"
            ),
            fca_value=format(calculation.fca_value, "f"),
            fca_status=calculation.status,
            component_summaries=[
                DfcComponentSummaryResponse.from_domain(summary)
                for summary in calculation.component_summaries
            ],
            audit_rows=[
                DfcAuditRowResponse.from_domain(row)
                for row in calculation.audit_rows
            ],
            pending_issues=[
                DfcPendingIssueResponse.from_domain(issue)
                for issue in calculation.pending_issues
            ],
            alerts=list(calculation.alerts),
            limitations=list(calculation.limitations),
            methodology_version_id=calculation.methodology_version_id,
        )


class DfcDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: DfcDecisionAction
    entry_number: str = Field(min_length=1, max_length=80)
    line_number: int = Field(ge=1)
    activity: DfcActivity | None = None
    component_code: str | None = Field(default=None, max_length=80)
    justification: str = Field(min_length=1, max_length=4000)
    evidence_id: str | None = Field(default=None, max_length=64)

    @model_validator(mode="after")
    def validate_action_contract(self) -> "DfcDecisionRequest":
        if self.action == DfcDecisionAction.INCLUDE and (
            self.activity in {None, DfcActivity.UNCLASSIFIED}
            or not self.component_code
        ):
            raise ValueError("included decision requires activity and component")
        if self.action == DfcDecisionAction.EXCLUDE and (
            self.activity is not None or self.component_code is not None
        ):
            raise ValueError("excluded decision cannot define activity or component")
        return self


class DfcApiErrorResponse(BaseModel):
    error_code: str
    message: str

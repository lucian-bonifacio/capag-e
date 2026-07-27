from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.application.roa_service import RoaResult
from app.domain import (
    ComponentStatus,
    RoaAuditRow,
    RoaBlock,
    RoaComponentSummary,
    RoaDecisionAction,
    RoaPendingGroup,
    RoaRowStatus,
)
from app.schemas.capag import CapagAssessmentResponse


class RoaComponentSummaryResponse(BaseModel):
    block: RoaBlock
    component_code: str
    component_label: str
    value: str
    account_count: int

    @classmethod
    def from_domain(
        cls,
        summary: RoaComponentSummary,
    ) -> "RoaComponentSummaryResponse":
        return cls(
            block=summary.block,
            component_code=summary.component_code,
            component_label=summary.component_label,
            value=format(summary.value, "f"),
            account_count=summary.account_count,
        )


class RoaAuditRowResponse(BaseModel):
    account_code: str
    account_name: str
    reference_code: str | None
    reference_description: str | None
    roa_block: RoaBlock | None
    component_roa: str | None
    component_label: str | None
    base_value: str
    signed_value: str
    treatment: str
    final_status: RoaRowStatus
    pending_reason: str | None
    evidence_id: str | None
    line_reference: int
    macrogroup: str | None
    required_evidence_type: str | None
    source_detail: str | None

    @classmethod
    def from_domain(cls, row: RoaAuditRow) -> "RoaAuditRowResponse":
        return cls(
            account_code=row.account_code,
            account_name=row.account_name,
            reference_code=row.reference_code,
            reference_description=row.reference_description,
            roa_block=row.roa_block,
            component_roa=row.component_roa,
            component_label=row.component_label,
            base_value=format(row.base_value, "f"),
            signed_value=format(row.signed_value, "f"),
            treatment=row.treatment,
            final_status=row.final_status,
            pending_reason=row.pending_reason,
            evidence_id=row.evidence_id,
            line_reference=row.line_reference,
            macrogroup=row.macrogroup,
            required_evidence_type=row.required_evidence_type,
            source_detail=row.source_detail,
        )


class RoaPendingGroupResponse(BaseModel):
    code: str
    message: str
    account_code: str | None
    reference_code: str | None
    blocks_roa: bool
    materiality_level: str | None
    evidence_id: str | None

    @classmethod
    def from_domain(cls, group: RoaPendingGroup) -> "RoaPendingGroupResponse":
        return cls(**group.to_snapshot())


class RoaCalculationResponse(BaseModel):
    exercise_year: int
    gross_revenue: str
    deductions: str
    revenue_taxes: str
    net_operating_revenue: str
    operating_costs: str
    operating_expenses: str
    financial_result: str
    non_operating_result: str
    cash_pressure_adjustments: str
    roa_preliminary: str
    roa_final: str
    roa_status: ComponentStatus
    component_summaries: list[RoaComponentSummaryResponse]
    audit_rows: list[RoaAuditRowResponse]
    pending_groups: list[RoaPendingGroupResponse]
    alerts: list[str]
    limitations: list[str]
    methodology_version_id: str
    capag_assessment: CapagAssessmentResponse | None

    @classmethod
    def from_result(cls, result: RoaResult) -> "RoaCalculationResponse":
        calculation = result.calculation
        return cls(
            exercise_year=calculation.exercise_year,
            gross_revenue=format(calculation.gross_revenue, "f"),
            deductions=format(calculation.deductions, "f"),
            revenue_taxes=format(calculation.revenue_taxes, "f"),
            net_operating_revenue=format(
                calculation.net_operating_revenue,
                "f",
            ),
            operating_costs=format(calculation.operating_costs, "f"),
            operating_expenses=format(calculation.operating_expenses, "f"),
            financial_result=format(calculation.financial_result, "f"),
            non_operating_result=format(calculation.non_operating_result, "f"),
            cash_pressure_adjustments=format(
                calculation.cash_pressure_adjustments,
                "f",
            ),
            roa_preliminary=format(calculation.roa_preliminary, "f"),
            roa_final=format(calculation.roa_final, "f"),
            roa_status=calculation.status,
            component_summaries=[
                RoaComponentSummaryResponse.from_domain(summary)
                for summary in calculation.component_summaries
            ],
            audit_rows=[
                RoaAuditRowResponse.from_domain(row)
                for row in calculation.audit_rows
            ],
            pending_groups=[
                RoaPendingGroupResponse.from_domain(group)
                for group in calculation.pending_groups
            ],
            alerts=list(calculation.alerts),
            limitations=list(calculation.limitations),
            methodology_version_id=calculation.methodology_version_id,
            capag_assessment=(
                CapagAssessmentResponse.from_domain(result.capag_assessment)
                if result.capag_assessment is not None
                else None
            ),
        )


class RoaDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: RoaDecisionAction
    account_code: str = Field(min_length=1, max_length=64)
    justification: str = Field(min_length=1, max_length=4000)
    evidence_id: str | None = Field(default=None, max_length=64)


class RoaApiErrorResponse(BaseModel):
    error_code: str
    message: str

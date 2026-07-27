from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from app.domain.capag import ComponentStatus


CENT = Decimal("0.01")


class RoaBlock(StrEnum):
    GROSS_REVENUE = "receita_bruta"
    DEDUCTIONS = "deducoes_receita"
    REVENUE_TAXES = "tributos_receita"
    OPERATING_COSTS = "custos_operacionais"
    OPERATING_EXPENSES = "despesas_operacionais"
    FINANCIAL_RESULT = "resultado_financeiro"
    NON_OPERATING_RESULT = "resultado_nao_operacional"
    CASH_PRESSURES = "pressoes_complementares_caixa"


class RoaRowStatus(StrEnum):
    INCLUDED = "incluido"
    EXCLUDED = "excluido"
    PENDING_REVIEW = "pendente_revisao"
    NO_RULE = "sem_regra"
    PENDING_EVIDENCE = "pendente_evidencia"
    MANUAL_DECISION_APPLIED = "decisao_manual_aplicada"


class RoaDecisionAction(StrEnum):
    INCLUDE = "incluir"
    EXCLUDE = "excluir"


@dataclass(frozen=True)
class RoaManualDecision:
    decision_id: str
    account_code: str
    action: RoaDecisionAction
    justification: str
    evidence_id: str | None
    decided_at: datetime
    methodology_version_id: str

    def __post_init__(self) -> None:
        for field_name in {
            "decision_id",
            "account_code",
            "justification",
            "methodology_version_id",
        }:
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} is required")
        if not isinstance(self.action, RoaDecisionAction):
            object.__setattr__(self, "action", RoaDecisionAction(self.action))
        if self.decided_at.tzinfo is None:
            raise ValueError("decided_at must include timezone")


@dataclass(frozen=True)
class RoaAccountInput:
    account_code: str
    account_name: str
    reference_code: str | None
    reference_description: str | None
    debit_amount: Decimal
    credit_amount: Decimal
    line_reference: int
    balance_nature: str | None = None

    def __post_init__(self) -> None:
        for field_name in {"account_code", "account_name"}:
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} is required")
        for field_name in {"debit_amount", "credit_amount"}:
            value = getattr(self, field_name)
            if not isinstance(value, Decimal):
                raise TypeError(f"{field_name} must be Decimal")
            if not value.is_finite() or value < Decimal("0"):
                raise ValueError(f"{field_name} must be finite and non-negative")
            object.__setattr__(self, field_name, value.quantize(CENT))
        if isinstance(self.line_reference, bool) or not isinstance(
            self.line_reference, int
        ):
            raise TypeError("line_reference must be int")
        if self.line_reference < 1:
            raise ValueError("line_reference must be positive")
        if self.balance_nature not in {None, "D", "C"}:
            raise ValueError("balance_nature must be D, C or None")


@dataclass(frozen=True)
class RoaCashPressureInput:
    pressure_id: str
    pressure_type: str
    account_code: str
    account_name: str
    reference_code: str | None
    amount: Decimal
    source_reference: str
    line_reference: int

    def __post_init__(self) -> None:
        for field_name in {
            "pressure_id",
            "pressure_type",
            "account_code",
            "account_name",
            "source_reference",
        }:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} is required")
        if not isinstance(self.amount, Decimal):
            raise TypeError("amount must be Decimal")
        if not self.amount.is_finite() or self.amount < Decimal("0"):
            raise ValueError("amount must be finite and non-negative")
        object.__setattr__(self, "amount", self.amount.quantize(CENT))
        if isinstance(self.line_reference, bool) or not isinstance(
            self.line_reference, int
        ):
            raise TypeError("line_reference must be int")
        if self.line_reference < 1:
            raise ValueError("line_reference must be positive")


@dataclass(frozen=True)
class RoaAuditRow:
    account_code: str
    account_name: str
    reference_code: str | None
    reference_description: str | None
    roa_block: RoaBlock | None
    component_roa: str | None
    component_label: str | None
    base_value: Decimal
    signed_value: Decimal
    treatment: str
    final_status: RoaRowStatus
    pending_reason: str | None
    evidence_id: str | None
    line_reference: int
    macrogroup: str | None
    required_evidence_type: str | None
    source_detail: str | None

    def __post_init__(self) -> None:
        if self.roa_block is not None and not isinstance(self.roa_block, RoaBlock):
            object.__setattr__(self, "roa_block", RoaBlock(self.roa_block))
        if not isinstance(self.final_status, RoaRowStatus):
            object.__setattr__(self, "final_status", RoaRowStatus(self.final_status))
        for field_name in {"base_value", "signed_value"}:
            value = getattr(self, field_name)
            if not isinstance(value, Decimal):
                raise TypeError(f"{field_name} must be Decimal")
            if not value.is_finite():
                raise ValueError(f"{field_name} must be finite")
            object.__setattr__(self, field_name, value.quantize(CENT))
        if self.base_value < Decimal("0"):
            raise ValueError("base_value must be non-negative")

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "account_code": self.account_code,
            "account_name": self.account_name,
            "reference_code": self.reference_code,
            "reference_description": self.reference_description,
            "roa_block": self.roa_block.value if self.roa_block else None,
            "component_roa": self.component_roa,
            "component_label": self.component_label,
            "base_value": format(self.base_value, "f"),
            "signed_value": format(self.signed_value, "f"),
            "treatment": self.treatment,
            "final_status": self.final_status.value,
            "pending_reason": self.pending_reason,
            "evidence_id": self.evidence_id,
            "line_reference": self.line_reference,
            "macrogroup": self.macrogroup,
            "required_evidence_type": self.required_evidence_type,
            "source_detail": self.source_detail,
        }


@dataclass(frozen=True)
class RoaComponentSummary:
    block: RoaBlock
    component_code: str
    component_label: str
    value: Decimal
    account_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.block, RoaBlock):
            object.__setattr__(self, "block", RoaBlock(self.block))
        if not isinstance(self.value, Decimal):
            raise TypeError("value must be Decimal")
        if not self.value.is_finite():
            raise ValueError("value must be finite")
        object.__setattr__(self, "value", self.value.quantize(CENT))

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "block": self.block.value,
            "component_code": self.component_code,
            "component_label": self.component_label,
            "value": format(self.value, "f"),
            "account_count": self.account_count,
        }


@dataclass(frozen=True)
class RoaPendingGroup:
    code: str
    message: str
    account_code: str | None
    reference_code: str | None
    blocks_roa: bool
    materiality_level: str | None = None
    evidence_id: str | None = None

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "account_code": self.account_code,
            "reference_code": self.reference_code,
            "blocks_roa": self.blocks_roa,
            "materiality_level": self.materiality_level,
            "evidence_id": self.evidence_id,
        }


@dataclass(frozen=True)
class RoaCalculation:
    exercise_year: int
    gross_revenue: Decimal
    deductions: Decimal
    revenue_taxes: Decimal
    net_operating_revenue: Decimal
    operating_costs: Decimal
    operating_expenses: Decimal
    financial_result: Decimal
    non_operating_result: Decimal
    cash_pressure_adjustments: Decimal
    roa_preliminary: Decimal
    roa_final: Decimal
    status: ComponentStatus
    component_summaries: tuple[RoaComponentSummary, ...]
    audit_rows: tuple[RoaAuditRow, ...]
    pending_groups: tuple[RoaPendingGroup, ...]
    alerts: tuple[str, ...]
    limitations: tuple[str, ...]
    methodology_version_id: str

    def __post_init__(self) -> None:
        if isinstance(self.exercise_year, bool) or not isinstance(
            self.exercise_year, int
        ):
            raise TypeError("exercise_year must be int")
        if not isinstance(self.status, ComponentStatus):
            object.__setattr__(self, "status", ComponentStatus(self.status))
        for field_name in {
            "gross_revenue",
            "deductions",
            "revenue_taxes",
            "net_operating_revenue",
            "operating_costs",
            "operating_expenses",
            "financial_result",
            "non_operating_result",
            "cash_pressure_adjustments",
            "roa_preliminary",
            "roa_final",
        }:
            value = getattr(self, field_name)
            if not isinstance(value, Decimal):
                raise TypeError(f"{field_name} must be Decimal")
            if not value.is_finite():
                raise ValueError(f"{field_name} must be finite")
            object.__setattr__(self, field_name, value.quantize(CENT))
        if not self.methodology_version_id.strip():
            raise ValueError("methodology_version_id is required")
        for field_name in {
            "component_summaries",
            "audit_rows",
            "pending_groups",
            "alerts",
            "limitations",
        }:
            object.__setattr__(self, field_name, tuple(getattr(self, field_name)))

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "exercise_year": self.exercise_year,
            "gross_revenue": format(self.gross_revenue, "f"),
            "deductions": format(self.deductions, "f"),
            "revenue_taxes": format(self.revenue_taxes, "f"),
            "net_operating_revenue": format(self.net_operating_revenue, "f"),
            "operating_costs": format(self.operating_costs, "f"),
            "operating_expenses": format(self.operating_expenses, "f"),
            "financial_result": format(self.financial_result, "f"),
            "non_operating_result": format(self.non_operating_result, "f"),
            "cash_pressure_adjustments": format(
                self.cash_pressure_adjustments, "f"
            ),
            "roa_preliminary": format(self.roa_preliminary, "f"),
            "roa_final": format(self.roa_final, "f"),
            "status": self.status.value,
            "component_summaries": [
                summary.to_snapshot() for summary in self.component_summaries
            ],
            "audit_rows": [row.to_snapshot() for row in self.audit_rows],
            "pending_groups": [group.to_snapshot() for group in self.pending_groups],
            "alerts": list(self.alerts),
            "limitations": list(self.limitations),
            "methodology_version_id": self.methodology_version_id,
        }

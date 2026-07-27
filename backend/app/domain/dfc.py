from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from app.domain.capag import ComponentStatus


CENT = Decimal("0.01")


class DfcActivity(StrEnum):
    OPERATIONAL = "operacional"
    INVESTMENT = "investimento"
    FINANCING = "financiamento"
    UNCLASSIFIED = "nao_classificado"


class CashFlowDirection(StrEnum):
    INFLOW = "entrada"
    OUTFLOW = "saida"


class DfcRowStatus(StrEnum):
    INCLUDED = "incluido"
    EXCLUDED = "excluido"
    UNCLASSIFIED = "nao_classificado"
    INCOMPATIBLE_FLOW = "fluxo_incompativel"
    PENDING_EVIDENCE = "pendente_evidencia"
    MANUAL_DECISION_APPLIED = "decisao_manual_aplicada"


class DfcDecisionAction(StrEnum):
    INCLUDE = "incluir"
    EXCLUDE = "excluir"


@dataclass(frozen=True)
class DfcEntryItem:
    account_code: str
    account_name: str
    reference_code: str | None
    amount: Decimal
    debit_credit_indicator: str
    history: str | None
    line_number: int

    def __post_init__(self) -> None:
        if not self.account_code.strip():
            raise ValueError("account_code is required")
        if not isinstance(self.amount, Decimal):
            raise TypeError("amount must be Decimal")
        if not self.amount.is_finite() or self.amount < Decimal("0"):
            raise ValueError("amount must be finite and non-negative")
        if self.debit_credit_indicator not in {"D", "C"}:
            raise ValueError("debit_credit_indicator must be D or C")
        if isinstance(self.line_number, bool) or not isinstance(self.line_number, int):
            raise TypeError("line_number must be int")
        if self.line_number < 1:
            raise ValueError("line_number must be positive")
        object.__setattr__(self, "amount", self.amount.quantize(CENT))


@dataclass(frozen=True)
class DfcEntry:
    entry_number: str
    entry_date: date | None
    items: tuple[DfcEntryItem, ...]

    def __post_init__(self) -> None:
        if not self.entry_number.strip():
            raise ValueError("entry_number is required")
        if not isinstance(self.items, tuple):
            raise TypeError("items must be tuple")


@dataclass(frozen=True)
class DfcAuditRow:
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
    movement_value: Decimal
    included_value: Decimal
    final_status: DfcRowStatus
    pending_reason: str | None
    history: str | None
    line_number: int

    def __post_init__(self) -> None:
        if not isinstance(self.cash_flow_direction, CashFlowDirection):
            object.__setattr__(
                self,
                "cash_flow_direction",
                CashFlowDirection(self.cash_flow_direction),
            )
        if not isinstance(self.dfc_activity, DfcActivity):
            object.__setattr__(self, "dfc_activity", DfcActivity(self.dfc_activity))
        if not isinstance(self.final_status, DfcRowStatus):
            object.__setattr__(self, "final_status", DfcRowStatus(self.final_status))
        for field_name in {"movement_value", "included_value"}:
            value = getattr(self, field_name)
            if not isinstance(value, Decimal):
                raise TypeError(f"{field_name} must be Decimal")
            if not value.is_finite():
                raise ValueError(f"{field_name} must be finite")
            object.__setattr__(self, field_name, value.quantize(CENT))
        if self.movement_value < Decimal("0"):
            raise ValueError("movement_value must be non-negative")

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "entry_number": self.entry_number,
            "entry_date": self.entry_date.isoformat() if self.entry_date else None,
            "cash_account_code": self.cash_account_code,
            "cash_flow_direction": self.cash_flow_direction.value,
            "counterparty_account_code": self.counterparty_account_code,
            "counterparty_account_name": self.counterparty_account_name,
            "counterparty_reference_code": self.counterparty_reference_code,
            "dfc_activity": self.dfc_activity.value,
            "dfc_component_code": self.dfc_component_code,
            "dfc_component_label": self.dfc_component_label,
            "movement_value": format(self.movement_value, "f"),
            "included_value": format(self.included_value, "f"),
            "final_status": self.final_status.value,
            "pending_reason": self.pending_reason,
            "history": self.history,
            "line_number": self.line_number,
        }


@dataclass(frozen=True)
class DfcManualAdjustment:
    decision_id: str
    value: Decimal
    validated: bool
    justification: str
    evidence_id: str | None

    def __post_init__(self) -> None:
        if not self.decision_id.strip():
            raise ValueError("decision_id is required")
        if not isinstance(self.value, Decimal):
            raise TypeError("value must be Decimal")
        if not self.value.is_finite():
            raise ValueError("value must be finite")
        if not self.justification.strip():
            raise ValueError("justification is required")
        object.__setattr__(self, "value", self.value.quantize(CENT))


@dataclass(frozen=True)
class DfcManualDecision:
    decision_id: str
    entry_number: str
    line_number: int
    action: DfcDecisionAction
    activity: DfcActivity | None
    component_code: str | None
    justification: str
    evidence_id: str | None
    decided_at: datetime
    methodology_version_id: str

    def __post_init__(self) -> None:
        for field_name in {"decision_id", "entry_number", "justification", "methodology_version_id"}:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} is required")
        if not isinstance(self.action, DfcDecisionAction):
            object.__setattr__(self, "action", DfcDecisionAction(self.action))
        if self.activity is not None and not isinstance(self.activity, DfcActivity):
            object.__setattr__(self, "activity", DfcActivity(self.activity))
        if self.action == DfcDecisionAction.INCLUDE and (
            self.activity in {None, DfcActivity.UNCLASSIFIED}
            or not self.component_code
        ):
            raise ValueError("included decision requires classified activity and component")
        if self.action == DfcDecisionAction.EXCLUDE and (
            self.activity is not None or self.component_code is not None
        ):
            raise ValueError("excluded decision cannot define activity or component")


@dataclass(frozen=True)
class DfcComponentSummary:
    activity: DfcActivity
    component_code: str
    component_label: str
    value: Decimal
    movement_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.activity, DfcActivity):
            object.__setattr__(self, "activity", DfcActivity(self.activity))
        if not isinstance(self.value, Decimal):
            raise TypeError("value must be Decimal")
        if not self.value.is_finite():
            raise ValueError("value must be finite")
        object.__setattr__(self, "value", self.value.quantize(CENT))

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "activity": self.activity.value,
            "component_code": self.component_code,
            "component_label": self.component_label,
            "value": format(self.value, "f"),
            "movement_count": self.movement_count,
        }


@dataclass(frozen=True)
class DfcPendingIssue:
    code: str
    message: str
    entry_number: str | None
    line_number: int | None
    materiality_level: str | None
    blocks_fca: bool

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "entry_number": self.entry_number,
            "line_number": self.line_number,
            "materiality_level": self.materiality_level,
            "blocks_fca": self.blocks_fca,
        }


@dataclass(frozen=True)
class DfcCalculation:
    exercise_year: int
    automatic_value: Decimal
    operational_flow: Decimal
    investment_flow: Decimal
    financing_flow: Decimal
    manual_adjustments_value: Decimal
    fca_value: Decimal
    status: ComponentStatus
    component_summaries: tuple[DfcComponentSummary, ...]
    audit_rows: tuple[DfcAuditRow, ...]
    pending_issues: tuple[DfcPendingIssue, ...]
    alerts: tuple[str, ...]
    limitations: tuple[str, ...]
    methodology_version_id: str

    def __post_init__(self) -> None:
        if isinstance(self.exercise_year, bool) or not isinstance(self.exercise_year, int):
            raise TypeError("exercise_year must be int")
        if not isinstance(self.status, ComponentStatus):
            object.__setattr__(self, "status", ComponentStatus(self.status))
        for field_name in {
            "automatic_value",
            "operational_flow",
            "investment_flow",
            "financing_flow",
            "manual_adjustments_value",
            "fca_value",
        }:
            value = getattr(self, field_name)
            if not isinstance(value, Decimal):
                raise TypeError(f"{field_name} must be Decimal")
            if not value.is_finite():
                raise ValueError(f"{field_name} must be finite")
            object.__setattr__(self, field_name, value.quantize(CENT))
        if not self.methodology_version_id.strip():
            raise ValueError("methodology_version_id is required")
        object.__setattr__(self, "component_summaries", tuple(self.component_summaries))
        object.__setattr__(self, "audit_rows", tuple(self.audit_rows))
        object.__setattr__(self, "pending_issues", tuple(self.pending_issues))
        object.__setattr__(self, "alerts", tuple(self.alerts))
        object.__setattr__(self, "limitations", tuple(self.limitations))

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "exercise_year": self.exercise_year,
            "automatic_value": format(self.automatic_value, "f"),
            "operational_flow": format(self.operational_flow, "f"),
            "investment_flow": format(self.investment_flow, "f"),
            "financing_flow": format(self.financing_flow, "f"),
            "manual_adjustments_value": format(self.manual_adjustments_value, "f"),
            "fca_value": format(self.fca_value, "f"),
            "status": self.status.value,
            "component_summaries": [
                summary.to_snapshot() for summary in self.component_summaries
            ],
            "audit_rows": [row.to_snapshot() for row in self.audit_rows],
            "pending_issues": [issue.to_snapshot() for issue in self.pending_issues],
            "alerts": list(self.alerts),
            "limitations": list(self.limitations),
            "methodology_version_id": self.methodology_version_id,
        }

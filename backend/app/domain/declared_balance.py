from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum


class DeclaredBalanceStatus(StrEnum):
    VALIDO = "VALIDO"
    DIVERGENTE = "DIVERGENTE"
    OBRIGATORIO_AUSENTE = "OBRIGATORIO_AUSENTE"
    ESTRUTURA_INVALIDA = "ESTRUTURA_INVALIDA"
    NAO_OBRIGATORIO = "NAO_OBRIGATORIO"


class BalanceLineStatus(StrEnum):
    CONCILIADA = "CONCILIADA"
    DIVERGENTE = "DIVERGENTE"
    SEM_I052 = "SEM_I052"
    SEM_SALDO_I155 = "SEM_SALDO_I155"


class BalanceRowStructuralStatus(StrEnum):
    VALIDA = "VALIDA"
    INVALIDA = "INVALIDA"


@dataclass(frozen=True)
class BalanceAccount:
    account_code: str
    account_name: str
    account_type: str | None


@dataclass(frozen=True)
class BalanceAggregationLink:
    account_code: str
    cost_center_code: str | None
    aggregation_code: str
    line_number: int


@dataclass(frozen=True)
class BalanceAccountValue:
    account_code: str
    cost_center_code: str | None
    period_end: date | None
    final_amount: Decimal
    final_debit_credit_indicator: str
    line_number: int


@dataclass(frozen=True)
class BalanceComponent:
    account_code: str
    account_name: str
    cost_center_code: str | None
    final_amount: Decimal | None
    final_debit_credit_indicator: str | None
    signed_final_amount: Decimal | None
    i052_line_number: int
    i155_line_number: int | None


@dataclass(frozen=True)
class BalanceStatementRow:
    aggregation_code: str | None
    aggregation_code_type: str | None
    aggregation_level: int | None
    parent_aggregation_code: str | None
    balance_group: str | None
    description: str
    initial_amount: Decimal
    initial_debit_credit_indicator: str | None
    final_amount: Decimal | None
    final_debit_credit_indicator: str | None
    explanatory_note_reference: str | None
    line_number: int


@dataclass(frozen=True)
class BalanceStatement:
    period_start: date
    period_end: date
    statement_id: str
    line_number: int
    has_j150: bool
    rows: tuple[BalanceStatementRow, ...]


@dataclass(frozen=True)
class DeclaredBalanceInput:
    year: int
    ecd_period_start: date
    ecd_period_end: date
    bookkeeping_forms: tuple[str, ...]
    closing_dates: tuple[date, ...]
    statements: tuple[BalanceStatement, ...]
    accounts: tuple[BalanceAccount, ...]
    aggregation_links: tuple[BalanceAggregationLink, ...]
    account_values: tuple[BalanceAccountValue, ...]


@dataclass(frozen=True)
class DeclaredBalanceRow:
    aggregation_code: str
    aggregation_code_type: str
    aggregation_level: int
    parent_aggregation_code: str | None
    balance_group: str
    description: str
    initial_amount: Decimal
    initial_debit_credit_indicator: str
    signed_initial_amount: Decimal | None
    final_amount: Decimal
    final_debit_credit_indicator: str
    signed_final_amount: Decimal | None
    explanatory_note_reference: str | None
    line_number: int
    structural_status: BalanceRowStructuralStatus
    reconciliation_status: BalanceLineStatus | None
    reconciled_amount: Decimal | None
    difference: Decimal | None
    component_count: int
    components: tuple[BalanceComponent, ...]
    children: tuple[DeclaredBalanceRow, ...]


@dataclass(frozen=True)
class DeclaredBalance:
    year: int
    status: DeclaredBalanceStatus
    is_blocking: bool
    j005_period_start: date | None
    j005_period_end: date | None
    assets_final_amount: Decimal | None
    liabilities_and_equity_final_amount: Decimal | None
    difference: Decimal | None
    rows: tuple[DeclaredBalanceRow, ...]
    limitations: tuple[str, ...]

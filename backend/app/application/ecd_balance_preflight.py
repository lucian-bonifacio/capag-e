from __future__ import annotations

from collections import defaultdict

from app.domain import (
    BalanceAccount,
    BalanceAccountValue,
    BalanceAggregationLink,
    BalanceStatement,
    BalanceStatementRow,
    DeclaredBalance,
    DeclaredBalanceInput,
    DeclaredBalanceStatus,
)
from app.engine import calculate_declared_balance
from app.io import ParsedEcd


IMPORT_REJECTED_BALANCE_STATUSES = frozenset(
    {
        DeclaredBalanceStatus.OBRIGATORIO_AUSENTE,
        DeclaredBalanceStatus.NAO_OBRIGATORIO,
        DeclaredBalanceStatus.ESTRUTURA_INVALIDA,
    }
)


IMPORT_REJECTION_MESSAGES = {
    DeclaredBalanceStatus.OBRIGATORIO_AUSENTE: (
        "ECD rejeitada: Balanco Patrimonial obrigatorio ausente. "
        "Envie uma ECD corrigida ou substituta."
    ),
    DeclaredBalanceStatus.NAO_OBRIGATORIO: (
        "ECD rejeitada: o arquivo nao cobre o encerramento anual necessario "
        "para analise CAPAG-E. Envie a ECD do exercicio encerrado contendo o Bloco J."
    ),
    DeclaredBalanceStatus.ESTRUTURA_INVALIDA: (
        "ECD rejeitada: o Balanco Patrimonial declarado no J100 nao possui "
        "estrutura valida para analise CAPAG-E. Envie a ECD anual transmitida/"
        "validada no PGE do SPED ou uma ECD substituta valida."
    ),
}


def calculate_import_balance_preflight(parsed_ecd: ParsedEcd) -> DeclaredBalance:
    return calculate_declared_balance(_balance_input_from_parsed_ecd(parsed_ecd))


def is_import_rejected_balance_status(status: DeclaredBalanceStatus) -> bool:
    return status in IMPORT_REJECTED_BALANCE_STATUSES


def import_rejection_message(status: DeclaredBalanceStatus) -> str:
    return IMPORT_REJECTION_MESSAGES[status]


def _balance_input_from_parsed_ecd(parsed_ecd: ParsedEcd) -> DeclaredBalanceInput:
    j100_by_statement: dict[int, list] = defaultdict(list)
    for row in parsed_ecd.j100_rows:
        if row.j005_line_number is not None:
            j100_by_statement[row.j005_line_number].append(row)

    j150_statement_lines = {
        row.j005_line_number
        for row in parsed_ecd.j150_presence
        if row.j005_line_number is not None
    }

    return DeclaredBalanceInput(
        year=parsed_ecd.header.period_end.year,
        ecd_period_start=parsed_ecd.header.period_start,
        ecd_period_end=parsed_ecd.header.period_end,
        bookkeeping_forms=tuple(
            row.bookkeeping_form for row in parsed_ecd.bookkeeping_i010
        ),
        closing_dates=tuple(row.closing_date for row in parsed_ecd.book_headers_i030),
        statements=tuple(
            BalanceStatement(
                period_start=statement.period_start,
                period_end=statement.period_end,
                statement_id=statement.statement_id,
                line_number=statement.line_number,
                has_j150=statement.line_number in j150_statement_lines,
                rows=tuple(
                    BalanceStatementRow(
                        aggregation_code=row.aggregation_code,
                        aggregation_code_type=row.aggregation_code_type,
                        aggregation_level=row.aggregation_level,
                        parent_aggregation_code=row.parent_aggregation_code,
                        balance_group=row.balance_group,
                        description=row.description,
                        initial_amount=row.initial_amount,
                        initial_debit_credit_indicator=(
                            row.initial_debit_credit_indicator
                        ),
                        final_amount=row.final_amount,
                        final_debit_credit_indicator=(
                            row.final_debit_credit_indicator
                        ),
                        explanatory_note_reference=row.explanatory_note_reference,
                        line_number=row.line_number,
                    )
                    for row in j100_by_statement.get(statement.line_number, [])
                ),
            )
            for statement in parsed_ecd.statements_j005
        ),
        accounts=tuple(
            BalanceAccount(
                account_code=account.account_code,
                account_name=account.account_name,
                account_type=account.account_type,
            )
            for account in parsed_ecd.accounts_i050
        ),
        aggregation_links=tuple(
            BalanceAggregationLink(
                account_code=link.account_code,
                cost_center_code=link.cost_center_code,
                aggregation_code=link.aggregation_code,
                line_number=link.line_number,
            )
            for link in parsed_ecd.aggregation_links_i052
        ),
        account_values=tuple(
            BalanceAccountValue(
                account_code=balance.account_code,
                cost_center_code=balance.cost_center_code,
                period_end=balance.period_end,
                final_amount=balance.final_balance,
                final_debit_credit_indicator=balance.final_balance_indicator,
                line_number=balance.line_number,
            )
            for balance in parsed_ecd.balances_i155
        ),
    )

from __future__ import annotations

from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain import (
    BalanceAccount,
    BalanceAccountValue,
    BalanceAggregationLink,
    BalanceStatement,
    BalanceStatementRow,
    DeclaredBalance,
    DeclaredBalanceInput,
)
from app.engine import calculate_declared_balance
from app.repositories import (
    AnalysisModel,
    EcdFileModel,
    EcdI010BookkeepingModel,
    EcdI030BookHeaderModel,
    EcdI050AccountModel,
    EcdI052AggregationLinkModel,
    EcdI155BalanceModel,
    EcdJ005StatementModel,
    EcdJ100BalanceRowModel,
    EcdJ150PresenceModel,
    ExerciseModel,
)


class DeclaredBalanceNotFound(LookupError):
    pass


class DeclaredBalanceUnavailable(RuntimeError):
    pass


def get_declared_balance(
    session: Session,
    *,
    analysis_id: str,
    year: int,
) -> DeclaredBalance:
    try:
        context = session.execute(
            select(ExerciseModel, EcdFileModel)
            .join(AnalysisModel, AnalysisModel.id == ExerciseModel.analysis_id)
            .join(EcdFileModel, EcdFileModel.id == AnalysisModel.ecd_file_id)
            .where(AnalysisModel.id == analysis_id)
            .where(ExerciseModel.year == year)
        ).one_or_none()
        if context is None:
            raise DeclaredBalanceNotFound("Declared balance context not found.")

        exercise, ecd_file = context
        bookkeeping = tuple(
            session.scalars(
                select(EcdI010BookkeepingModel)
                .where(EcdI010BookkeepingModel.exercise_id == exercise.id)
                .order_by(EcdI010BookkeepingModel.line_number)
            )
        )
        headers = tuple(
            session.scalars(
                select(EcdI030BookHeaderModel)
                .where(EcdI030BookHeaderModel.exercise_id == exercise.id)
                .order_by(EcdI030BookHeaderModel.line_number)
            )
        )
        accounts = tuple(
            session.scalars(
                select(EcdI050AccountModel)
                .where(EcdI050AccountModel.exercise_id == exercise.id)
                .order_by(EcdI050AccountModel.line_number)
            )
        )
        links = tuple(
            session.scalars(
                select(EcdI052AggregationLinkModel)
                .where(EcdI052AggregationLinkModel.exercise_id == exercise.id)
                .order_by(EcdI052AggregationLinkModel.line_number)
            )
        )
        balances = tuple(
            session.scalars(
                select(EcdI155BalanceModel)
                .where(EcdI155BalanceModel.exercise_id == exercise.id)
                .order_by(EcdI155BalanceModel.line_number)
            )
        )
        statements = tuple(
            session.scalars(
                select(EcdJ005StatementModel)
                .where(EcdJ005StatementModel.exercise_id == exercise.id)
                .order_by(EcdJ005StatementModel.line_number)
            )
        )
        j100_rows = tuple(
            session.scalars(
                select(EcdJ100BalanceRowModel)
                .where(EcdJ100BalanceRowModel.exercise_id == exercise.id)
                .order_by(EcdJ100BalanceRowModel.line_number)
            )
        )
        j150_rows = tuple(
            session.scalars(
                select(EcdJ150PresenceModel)
                .where(EcdJ150PresenceModel.exercise_id == exercise.id)
                .order_by(EcdJ150PresenceModel.line_number)
            )
        )
    except DeclaredBalanceNotFound:
        raise
    except SQLAlchemyError as exc:
        raise DeclaredBalanceUnavailable("Declared balance query failed.") from exc

    j100_by_statement: dict[int, list[EcdJ100BalanceRowModel]] = defaultdict(list)
    for row in j100_rows:
        if row.statement_id is not None:
            j100_by_statement[row.statement_id].append(row)
    j150_statement_ids = {
        row.statement_id for row in j150_rows if row.statement_id is not None
    }

    source = DeclaredBalanceInput(
        year=year,
        ecd_period_start=ecd_file.period_start,
        ecd_period_end=ecd_file.period_end,
        bookkeeping_forms=tuple(row.bookkeeping_form for row in bookkeeping),
        closing_dates=tuple(row.closing_date for row in headers),
        statements=tuple(
            BalanceStatement(
                period_start=statement.period_start,
                period_end=statement.period_end,
                statement_id=statement.statement_id,
                line_number=statement.line_number,
                has_j150=statement.id in j150_statement_ids,
                rows=tuple(
                    BalanceStatementRow(
                        aggregation_code=row.aggregation_code,
                        aggregation_code_type=row.aggregation_code_type,
                        aggregation_level=row.aggregation_level,
                        parent_aggregation_code=row.parent_aggregation_code,
                        balance_group=row.balance_group,
                        description=row.description,
                        initial_amount=row.initial_amount,
                        initial_debit_credit_indicator=row.initial_debit_credit_indicator,
                        final_amount=row.final_amount,
                        final_debit_credit_indicator=row.final_debit_credit_indicator,
                        explanatory_note_reference=row.explanatory_note_reference,
                        line_number=row.line_number,
                    )
                    for row in j100_by_statement.get(statement.id, [])
                ),
            )
            for statement in statements
        ),
        accounts=tuple(
            BalanceAccount(
                account_code=account.account_code,
                account_name=account.account_name,
                account_type=account.account_type,
            )
            for account in accounts
        ),
        aggregation_links=tuple(
            BalanceAggregationLink(
                account_code=link.account_code,
                cost_center_code=link.cost_center_code,
                aggregation_code=link.aggregation_code,
                line_number=link.line_number,
            )
            for link in links
        ),
        account_values=tuple(
            BalanceAccountValue(
                account_code=balance.account_code,
                cost_center_code=balance.cost_center_code,
                period_end=(
                    balance.balance_period.period_end
                    if balance.balance_period is not None
                    else None
                ),
                final_amount=balance.final_balance,
                final_debit_credit_indicator=balance.final_balance_indicator,
                line_number=balance.line_number,
            )
            for balance in balances
        ),
    )
    return calculate_declared_balance(source)


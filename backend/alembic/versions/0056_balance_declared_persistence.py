"""persist original ECD and declared balance records

Revision ID: 0056_balance_declared
Revises: 0055_roa_calculations
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0056_balance_declared"
down_revision: Union[str, None] = "0055_roa_calculations"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("ecd_files", sa.Column("original_content", sa.LargeBinary(), nullable=True))
    op.add_column("ecd_files", sa.Column("content_size", sa.BigInteger(), nullable=True))
    op.add_column("ecd_files", sa.Column("parser_version", sa.String(length=40), nullable=True))
    op.add_column(
        "ecd_files",
        sa.Column("reprocessed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_ecd_files_parser_version", "ecd_files", ["parser_version"], unique=False)

    op.create_table(
        "ecd_i010_bookkeeping",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("bookkeeping_form", sa.String(length=1), nullable=False),
        sa.Column("bookkeeping_version", sa.String(length=40), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ecd_i010_bookkeeping_exercise_id",
        "ecd_i010_bookkeeping",
        ["exercise_id"],
        unique=False,
    )

    op.create_table(
        "ecd_i030_book_headers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("closing_date", sa.Date(), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ecd_i030_book_headers_exercise_id",
        "ecd_i030_book_headers",
        ["exercise_id"],
        unique=False,
    )

    op.create_table(
        "ecd_i052_aggregation_links",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("cost_center_code", sa.String(length=64), nullable=True),
        sa.Column("aggregation_code", sa.String(length=64), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["ecd_i050_accounts.id"]),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "exercise_id",
        "account_id",
        "account_code",
        "cost_center_code",
        "aggregation_code",
    ):
        op.create_index(
            f"ix_ecd_i052_aggregation_links_{column}",
            "ecd_i052_aggregation_links",
            [column],
            unique=False,
        )

    op.create_table(
        "ecd_i150_balance_periods",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ecd_i150_balance_periods_exercise_id",
        "ecd_i150_balance_periods",
        ["exercise_id"],
        unique=False,
    )

    op.add_column(
        "ecd_i155_balances",
        sa.Column("balance_period_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "ecd_i155_balances",
        sa.Column("cost_center_code", sa.String(length=64), nullable=True),
    )
    op.create_foreign_key(
        "fk_i155_balance_period",
        "ecd_i155_balances",
        "ecd_i150_balance_periods",
        ["balance_period_id"],
        ["id"],
    )
    op.create_index(
        "ix_ecd_i155_balances_balance_period_id",
        "ecd_i155_balances",
        ["balance_period_id"],
        unique=False,
    )
    op.create_index(
        "ix_ecd_i155_balances_cost_center_code",
        "ecd_i155_balances",
        ["cost_center_code"],
        unique=False,
    )

    op.create_table(
        "ecd_j005_statements",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("statement_id", sa.String(length=20), nullable=False),
        sa.Column("statement_header", sa.Text(), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("exercise_id", "period_end", "statement_id"):
        op.create_index(
            f"ix_ecd_j005_statements_{column}",
            "ecd_j005_statements",
            [column],
            unique=False,
        )

    op.drop_index(
        "ix_ecd_j100_balance_rows_account_code",
        table_name="ecd_j100_balance_rows",
    )
    op.alter_column(
        "ecd_j100_balance_rows",
        "account_code",
        new_column_name="aggregation_code",
    )
    op.alter_column(
        "ecd_j100_balance_rows",
        "amount",
        new_column_name="initial_amount",
    )
    op.alter_column(
        "ecd_j100_balance_rows",
        "amount_indicator",
        new_column_name="initial_debit_credit_indicator",
    )
    op.add_column(
        "ecd_j100_balance_rows",
        sa.Column("statement_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "ecd_j100_balance_rows",
        sa.Column("aggregation_code_type", sa.String(length=1), nullable=True),
    )
    op.add_column(
        "ecd_j100_balance_rows",
        sa.Column("aggregation_level", sa.Integer(), nullable=True),
    )
    op.add_column(
        "ecd_j100_balance_rows",
        sa.Column("parent_aggregation_code", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "ecd_j100_balance_rows",
        sa.Column("balance_group", sa.String(length=1), nullable=True),
    )
    op.add_column(
        "ecd_j100_balance_rows",
        sa.Column("final_amount", sa.Numeric(18, 2), nullable=True),
    )
    op.add_column(
        "ecd_j100_balance_rows",
        sa.Column("final_debit_credit_indicator", sa.String(length=1), nullable=True),
    )
    op.add_column(
        "ecd_j100_balance_rows",
        sa.Column("explanatory_note_reference", sa.Text(), nullable=True),
    )
    op.create_foreign_key(
        "fk_j100_statement",
        "ecd_j100_balance_rows",
        "ecd_j005_statements",
        ["statement_id"],
        ["id"],
    )
    for column in (
        "statement_id",
        "aggregation_code",
        "parent_aggregation_code",
        "balance_group",
    ):
        op.create_index(
            f"ix_ecd_j100_balance_rows_{column}",
            "ecd_j100_balance_rows",
            [column],
            unique=False,
        )

    op.create_table(
        "ecd_j150_presence",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("statement_id", sa.Integer(), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.ForeignKeyConstraint(["statement_id"], ["ecd_j005_statements.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ecd_j150_presence_exercise_id",
        "ecd_j150_presence",
        ["exercise_id"],
        unique=False,
    )
    op.create_index(
        "ix_ecd_j150_presence_statement_id",
        "ecd_j150_presence",
        ["statement_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ecd_j150_presence_statement_id", table_name="ecd_j150_presence")
    op.drop_index("ix_ecd_j150_presence_exercise_id", table_name="ecd_j150_presence")
    op.drop_table("ecd_j150_presence")

    for column in (
        "balance_group",
        "parent_aggregation_code",
        "aggregation_code",
        "statement_id",
    ):
        op.drop_index(
            f"ix_ecd_j100_balance_rows_{column}",
            table_name="ecd_j100_balance_rows",
        )
    op.drop_constraint(
        "fk_j100_statement",
        "ecd_j100_balance_rows",
        type_="foreignkey",
    )
    for column in (
        "explanatory_note_reference",
        "final_debit_credit_indicator",
        "final_amount",
        "balance_group",
        "parent_aggregation_code",
        "aggregation_level",
        "aggregation_code_type",
        "statement_id",
    ):
        op.drop_column("ecd_j100_balance_rows", column)
    op.alter_column(
        "ecd_j100_balance_rows",
        "initial_debit_credit_indicator",
        new_column_name="amount_indicator",
    )
    op.alter_column(
        "ecd_j100_balance_rows",
        "initial_amount",
        new_column_name="amount",
    )
    op.alter_column(
        "ecd_j100_balance_rows",
        "aggregation_code",
        new_column_name="account_code",
    )
    op.create_index(
        "ix_ecd_j100_balance_rows_account_code",
        "ecd_j100_balance_rows",
        ["account_code"],
        unique=False,
    )

    for column in ("statement_id", "period_end", "exercise_id"):
        op.drop_index(
            f"ix_ecd_j005_statements_{column}",
            table_name="ecd_j005_statements",
        )
    op.drop_table("ecd_j005_statements")

    op.drop_index(
        "ix_ecd_i155_balances_cost_center_code",
        table_name="ecd_i155_balances",
    )
    op.drop_index(
        "ix_ecd_i155_balances_balance_period_id",
        table_name="ecd_i155_balances",
    )
    op.drop_constraint(
        "fk_i155_balance_period",
        "ecd_i155_balances",
        type_="foreignkey",
    )
    op.drop_column("ecd_i155_balances", "cost_center_code")
    op.drop_column("ecd_i155_balances", "balance_period_id")

    op.drop_index(
        "ix_ecd_i150_balance_periods_exercise_id",
        table_name="ecd_i150_balance_periods",
    )
    op.drop_table("ecd_i150_balance_periods")

    for column in (
        "aggregation_code",
        "cost_center_code",
        "account_code",
        "account_id",
        "exercise_id",
    ):
        op.drop_index(
            f"ix_ecd_i052_aggregation_links_{column}",
            table_name="ecd_i052_aggregation_links",
        )
    op.drop_table("ecd_i052_aggregation_links")

    op.drop_index(
        "ix_ecd_i030_book_headers_exercise_id",
        table_name="ecd_i030_book_headers",
    )
    op.drop_table("ecd_i030_book_headers")
    op.drop_index(
        "ix_ecd_i010_bookkeeping_exercise_id",
        table_name="ecd_i010_bookkeeping",
    )
    op.drop_table("ecd_i010_bookkeeping")

    op.drop_index("ix_ecd_files_parser_version", table_name="ecd_files")
    op.drop_column("ecd_files", "reprocessed_at")
    op.drop_column("ecd_files", "parser_version")
    op.drop_column("ecd_files", "content_size")
    op.drop_column("ecd_files", "original_content")

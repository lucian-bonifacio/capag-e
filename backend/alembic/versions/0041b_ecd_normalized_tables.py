"""create normalized ecd import tables

Revision ID: 0041b_ecd_normalized_tables
Revises: 0038_declared_account_snapshots
Create Date: 2026-07-06
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0041b_ecd_normalized_tables"
down_revision: Union[str, None] = "0038_declared_account_snapshots"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("tax_id", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tax_id"),
    )
    op.create_index("ix_companies_tax_id", "companies", ["tax_id"], unique=False)

    op.create_table(
        "ecd_files",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("company_id", sa.String(length=64), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("content_hash", sa.String(length=128), nullable=False),
        sa.Column("layout", sa.String(length=40), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("imported_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("content_hash"),
    )
    op.create_index("ix_ecd_files_company_id", "ecd_files", ["company_id"], unique=False)
    op.create_index("ix_ecd_files_content_hash", "ecd_files", ["content_hash"], unique=False)
    op.create_index("ix_ecd_files_layout", "ecd_files", ["layout"], unique=False)

    op.create_table(
        "analyses",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("company_id", sa.String(length=64), nullable=False),
        sa.Column("ecd_file_id", sa.String(length=64), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["ecd_file_id"], ["ecd_files.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analyses_company_id", "analyses", ["company_id"], unique=False)
    op.create_index("ix_analyses_ecd_file_id", "analyses", ["ecd_file_id"], unique=False)
    op.create_index("ix_analyses_methodology_version_id", "analyses", ["methodology_version_id"], unique=False)
    op.create_index("ix_analyses_status", "analyses", ["status"], unique=False)

    op.create_table(
        "analysis_exercises",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_id", sa.String(length=64), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=True),
        sa.ForeignKeyConstraint(["analysis_id"], ["analyses.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_id", "year", name="uq_analysis_exercises_year"),
    )
    op.create_index("ix_analysis_exercises_analysis_id", "analysis_exercises", ["analysis_id"], unique=False)
    op.create_index("ix_analysis_exercises_status", "analysis_exercises", ["status"], unique=False)
    op.create_index("ix_analysis_exercises_year", "analysis_exercises", ["year"], unique=False)

    op.create_table(
        "ecd_i050_accounts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("account_name", sa.String(length=255), nullable=False),
        sa.Column("account_type", sa.String(length=20), nullable=True),
        sa.Column("account_nature", sa.String(length=20), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("parent_account_code", sa.String(length=64), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("exercise_id", "account_code", name="uq_i050_account"),
    )
    op.create_index("ix_ecd_i050_accounts_account_code", "ecd_i050_accounts", ["account_code"], unique=False)
    op.create_index("ix_ecd_i050_accounts_exercise_id", "ecd_i050_accounts", ["exercise_id"], unique=False)

    op.create_table(
        "ecd_i051_reference_links",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("reference_code", sa.String(length=64), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ecd_i051_reference_links_account_code", "ecd_i051_reference_links", ["account_code"], unique=False)
    op.create_index("ix_ecd_i051_reference_links_exercise_id", "ecd_i051_reference_links", ["exercise_id"], unique=False)
    op.create_index("ix_ecd_i051_reference_links_reference_code", "ecd_i051_reference_links", ["reference_code"], unique=False)

    op.create_table(
        "ecd_i155_balances",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("initial_balance", sa.Numeric(18, 2), nullable=False),
        sa.Column("initial_balance_indicator", sa.String(length=1), nullable=False),
        sa.Column("debit_amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("credit_amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("final_balance", sa.Numeric(18, 2), nullable=False),
        sa.Column("final_balance_indicator", sa.String(length=1), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ecd_i155_balances_account_code", "ecd_i155_balances", ["account_code"], unique=False)
    op.create_index("ix_ecd_i155_balances_exercise_id", "ecd_i155_balances", ["exercise_id"], unique=False)

    op.create_table(
        "ecd_i200_entries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("entry_number", sa.String(length=80), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=True),
        sa.Column("total_amount", sa.Numeric(18, 2), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ecd_i200_entries_entry_number", "ecd_i200_entries", ["entry_number"], unique=False)
    op.create_index("ix_ecd_i200_entries_exercise_id", "ecd_i200_entries", ["exercise_id"], unique=False)

    op.create_table(
        "ecd_j100_balance_rows",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("amount_indicator", sa.String(length=1), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ecd_j100_balance_rows_account_code", "ecd_j100_balance_rows", ["account_code"], unique=False)
    op.create_index("ix_ecd_j100_balance_rows_exercise_id", "ecd_j100_balance_rows", ["exercise_id"], unique=False)

    op.create_table(
        "ecd_i250_entry_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("counterparty_account_code", sa.String(length=64), nullable=True),
        sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("debit_credit_indicator", sa.String(length=1), nullable=True),
        sa.Column("history", sa.Text(), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_line", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["entry_id"], ["ecd_i200_entries.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ecd_i250_entry_items_account_code", "ecd_i250_entry_items", ["account_code"], unique=False)
    op.create_index("ix_ecd_i250_entry_items_entry_id", "ecd_i250_entry_items", ["entry_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_ecd_i250_entry_items_entry_id", table_name="ecd_i250_entry_items")
    op.drop_index("ix_ecd_i250_entry_items_account_code", table_name="ecd_i250_entry_items")
    op.drop_table("ecd_i250_entry_items")
    op.drop_index("ix_ecd_j100_balance_rows_exercise_id", table_name="ecd_j100_balance_rows")
    op.drop_index("ix_ecd_j100_balance_rows_account_code", table_name="ecd_j100_balance_rows")
    op.drop_table("ecd_j100_balance_rows")
    op.drop_index("ix_ecd_i200_entries_exercise_id", table_name="ecd_i200_entries")
    op.drop_index("ix_ecd_i200_entries_entry_number", table_name="ecd_i200_entries")
    op.drop_table("ecd_i200_entries")
    op.drop_index("ix_ecd_i155_balances_exercise_id", table_name="ecd_i155_balances")
    op.drop_index("ix_ecd_i155_balances_account_code", table_name="ecd_i155_balances")
    op.drop_table("ecd_i155_balances")
    op.drop_index("ix_ecd_i051_reference_links_reference_code", table_name="ecd_i051_reference_links")
    op.drop_index("ix_ecd_i051_reference_links_exercise_id", table_name="ecd_i051_reference_links")
    op.drop_index("ix_ecd_i051_reference_links_account_code", table_name="ecd_i051_reference_links")
    op.drop_table("ecd_i051_reference_links")
    op.drop_index("ix_ecd_i050_accounts_exercise_id", table_name="ecd_i050_accounts")
    op.drop_index("ix_ecd_i050_accounts_account_code", table_name="ecd_i050_accounts")
    op.drop_table("ecd_i050_accounts")
    op.drop_index("ix_analysis_exercises_year", table_name="analysis_exercises")
    op.drop_index("ix_analysis_exercises_status", table_name="analysis_exercises")
    op.drop_index("ix_analysis_exercises_analysis_id", table_name="analysis_exercises")
    op.drop_table("analysis_exercises")
    op.drop_index("ix_analyses_status", table_name="analyses")
    op.drop_index("ix_analyses_methodology_version_id", table_name="analyses")
    op.drop_index("ix_analyses_ecd_file_id", table_name="analyses")
    op.drop_index("ix_analyses_company_id", table_name="analyses")
    op.drop_table("analyses")
    op.drop_index("ix_ecd_files_layout", table_name="ecd_files")
    op.drop_index("ix_ecd_files_content_hash", table_name="ecd_files")
    op.drop_index("ix_ecd_files_company_id", table_name="ecd_files")
    op.drop_table("ecd_files")
    op.drop_index("ix_companies_tax_id", table_name="companies")
    op.drop_table("companies")

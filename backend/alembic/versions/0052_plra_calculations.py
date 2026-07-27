"""create PLRA calculation snapshots

Revision ID: 0052_plra_calculations
Revises: 0051_capag_assessments
Create Date: 2026-07-24
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0052_plra_calculations"
down_revision: Union[str, None] = "0051_capag_assessments"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "capag_assessments",
        sa.Column("invalidated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_capag_assessments_invalidated_at",
        "capag_assessments",
        ["invalidated_at"],
        unique=False,
    )
    op.create_table(
        "plra_calculations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_year", sa.Integer(), nullable=False),
        sa.Column("gross_assets_value", sa.Numeric(18, 2), nullable=False),
        sa.Column(
            "gross_economic_liabilities_value", sa.Numeric(18, 2), nullable=False
        ),
        sa.Column("adjusted_assets_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("plr_gross_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("plra_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("plra_status", sa.String(length=40), nullable=False),
        sa.Column("calculation_formula", sa.Text(), nullable=False),
        sa.Column("pending_accounts_json", sa.JSON(), nullable=False),
        sa.Column("warnings_json", sa.JSON(), nullable=False),
        sa.Column("limitations_json", sa.JSON(), nullable=False),
        sa.Column("blocking_issues_json", sa.JSON(), nullable=False),
        sa.Column("j100_reconciliation_status", sa.String(length=80), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "exercise_id",
        "analysis_id",
        "exercise_year",
        "plra_status",
        "methodology_version_id",
    ):
        op.create_index(
            f"ix_plra_calculations_{column}",
            "plra_calculations",
            [column],
            unique=False,
        )
    op.create_table(
        "plra_audit_rows",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("calculation_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("account_name", sa.String(length=255), nullable=False),
        sa.Column("declared_reference_code", sa.String(length=64), nullable=True),
        sa.Column("methodology_rule_id", sa.String(length=120), nullable=True),
        sa.Column("methodology_group", sa.String(length=80), nullable=True),
        sa.Column("macrogroup", sa.String(length=80), nullable=True),
        sa.Column("base_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("inclusion_status", sa.String(length=50), nullable=False),
        sa.Column("default_discount_percent", sa.Numeric(8, 6), nullable=True),
        sa.Column("default_economic_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("validated_valuation_value", sa.Numeric(18, 2), nullable=True),
        sa.Column("final_economic_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("decision_status", sa.String(length=40), nullable=False),
        sa.Column("evidence_status", sa.String(length=40), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["calculation_id"], ["plra_calculations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "calculation_id",
        "account_code",
        "declared_reference_code",
        "inclusion_status",
        "methodology_version_id",
    ):
        op.create_index(
            f"ix_plra_audit_rows_{column}",
            "plra_audit_rows",
            [column],
            unique=False,
        )


def downgrade() -> None:
    for column in (
        "methodology_version_id",
        "inclusion_status",
        "declared_reference_code",
        "account_code",
        "calculation_id",
    ):
        op.drop_index(
            f"ix_plra_audit_rows_{column}", table_name="plra_audit_rows"
        )
    op.drop_table("plra_audit_rows")
    for column in (
        "methodology_version_id",
        "plra_status",
        "exercise_year",
        "analysis_id",
        "exercise_id",
    ):
        op.drop_index(
            f"ix_plra_calculations_{column}", table_name="plra_calculations"
        )
    op.drop_table("plra_calculations")
    op.drop_index(
        "ix_capag_assessments_invalidated_at", table_name="capag_assessments"
    )
    op.drop_column("capag_assessments", "invalidated_at")


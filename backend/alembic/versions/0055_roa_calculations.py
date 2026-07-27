"""create ROA calculations, audit rows and manual decisions

Revision ID: 0055_roa_calculations
Revises: 0054_dfc_calculations
Create Date: 2026-07-24
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0055_roa_calculations"
down_revision: Union[str, None] = "0054_dfc_calculations"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roa_calculations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_year", sa.Integer(), nullable=False),
        sa.Column("gross_revenue", sa.Numeric(18, 2), nullable=False),
        sa.Column("deductions", sa.Numeric(18, 2), nullable=False),
        sa.Column("revenue_taxes", sa.Numeric(18, 2), nullable=False),
        sa.Column("net_operating_revenue", sa.Numeric(18, 2), nullable=False),
        sa.Column("operating_costs", sa.Numeric(18, 2), nullable=False),
        sa.Column("operating_expenses", sa.Numeric(18, 2), nullable=False),
        sa.Column("financial_result", sa.Numeric(18, 2), nullable=False),
        sa.Column("non_operating_result", sa.Numeric(18, 2), nullable=False),
        sa.Column("cash_pressure_adjustments", sa.Numeric(18, 2), nullable=False),
        sa.Column("roa_preliminary", sa.Numeric(18, 2), nullable=False),
        sa.Column("roa_final", sa.Numeric(18, 2), nullable=False),
        sa.Column("roa_status", sa.String(length=40), nullable=False),
        sa.Column("alerts_json", sa.JSON(), nullable=False),
        sa.Column("limitations_json", sa.JSON(), nullable=False),
        sa.Column("pending_groups_json", sa.JSON(), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.Column(
            "calculated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("invalidated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "exercise_id",
        "analysis_id",
        "exercise_year",
        "roa_status",
        "methodology_version_id",
        "invalidated_at",
    ):
        op.create_index(
            f"ix_roa_calculations_{column}",
            "roa_calculations",
            [column],
            unique=False,
        )

    op.create_table(
        "roa_audit_rows",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("calculation_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("reference_code", sa.String(length=64), nullable=True),
        sa.Column("roa_block", sa.String(length=50), nullable=True),
        sa.Column("component_roa", sa.String(length=80), nullable=True),
        sa.Column("base_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("signed_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("final_status", sa.String(length=50), nullable=False),
        sa.Column("pending_reason", sa.Text(), nullable=True),
        sa.Column("evidence_id", sa.String(length=64), nullable=True),
        sa.Column("line_reference", sa.Integer(), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["calculation_id"], ["roa_calculations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "calculation_id",
        "account_code",
        "reference_code",
        "roa_block",
        "component_roa",
        "final_status",
    ):
        op.create_index(
            f"ix_roa_audit_rows_{column}",
            "roa_audit_rows",
            [column],
            unique=False,
        )

    op.create_table(
        "roa_manual_decisions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("decision_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=20), nullable=False),
        sa.Column("justification", sa.Text(), nullable=False),
        sa.Column("evidence_id", sa.String(length=64), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.ForeignKeyConstraint(
            ["evidence_id"], ["adjustment_evidences.evidence_id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("decision_id"),
    )
    for column in (
        "decision_id",
        "exercise_id",
        "account_code",
        "methodology_version_id",
    ):
        op.create_index(
            f"ix_roa_manual_decisions_{column}",
            "roa_manual_decisions",
            [column],
            unique=False,
        )


def downgrade() -> None:
    for column in (
        "methodology_version_id",
        "account_code",
        "exercise_id",
        "decision_id",
    ):
        op.drop_index(
            f"ix_roa_manual_decisions_{column}",
            table_name="roa_manual_decisions",
        )
    op.drop_table("roa_manual_decisions")
    for column in (
        "final_status",
        "component_roa",
        "roa_block",
        "reference_code",
        "account_code",
        "calculation_id",
    ):
        op.drop_index(
            f"ix_roa_audit_rows_{column}",
            table_name="roa_audit_rows",
        )
    op.drop_table("roa_audit_rows")
    for column in (
        "invalidated_at",
        "methodology_version_id",
        "roa_status",
        "exercise_year",
        "analysis_id",
        "exercise_id",
    ):
        op.drop_index(
            f"ix_roa_calculations_{column}",
            table_name="roa_calculations",
        )
    op.drop_table("roa_calculations")

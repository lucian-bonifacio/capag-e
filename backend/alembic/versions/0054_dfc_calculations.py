"""create DFC calculations, audit rows and manual decisions

Revision ID: 0054_dfc_calculations
Revises: 0053_evidences_assets
Create Date: 2026-07-24
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0054_dfc_calculations"
down_revision: Union[str, None] = "0053_evidences_assets"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dfc_calculations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_year", sa.Integer(), nullable=False),
        sa.Column("automatic_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("operational_flow", sa.Numeric(18, 2), nullable=False),
        sa.Column("investment_flow", sa.Numeric(18, 2), nullable=False),
        sa.Column("financing_flow", sa.Numeric(18, 2), nullable=False),
        sa.Column("manual_adjustments_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("fca_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("fca_status", sa.String(length=40), nullable=False),
        sa.Column("alerts_json", sa.JSON(), nullable=False),
        sa.Column("limitations_json", sa.JSON(), nullable=False),
        sa.Column("pending_issues_json", sa.JSON(), nullable=False),
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
        "fca_status",
        "methodology_version_id",
        "invalidated_at",
    ):
        op.create_index(
            f"ix_dfc_calculations_{column}",
            "dfc_calculations",
            [column],
            unique=False,
        )
    op.create_table(
        "dfc_audit_rows",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("calculation_id", sa.Integer(), nullable=False),
        sa.Column("entry_number", sa.String(length=80), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=True),
        sa.Column("cash_account_code", sa.String(length=64), nullable=False),
        sa.Column("cash_flow_direction", sa.String(length=20), nullable=False),
        sa.Column("counterparty_account_code", sa.String(length=64), nullable=False),
        sa.Column("counterparty_reference_code", sa.String(length=64), nullable=True),
        sa.Column("dfc_activity", sa.String(length=30), nullable=False),
        sa.Column("dfc_component_code", sa.String(length=80), nullable=True),
        sa.Column("movement_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("included_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("final_status", sa.String(length=50), nullable=False),
        sa.Column("pending_reason", sa.Text(), nullable=True),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["calculation_id"], ["dfc_calculations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "calculation_id",
        "entry_number",
        "counterparty_account_code",
        "counterparty_reference_code",
        "dfc_activity",
        "dfc_component_code",
        "final_status",
    ):
        op.create_index(
            f"ix_dfc_audit_rows_{column}",
            "dfc_audit_rows",
            [column],
            unique=False,
        )
    op.create_table(
        "dfc_manual_decisions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("decision_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("entry_number", sa.String(length=80), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=20), nullable=False),
        sa.Column("activity", sa.String(length=30), nullable=True),
        sa.Column("component_code", sa.String(length=80), nullable=True),
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
        "entry_number",
        "methodology_version_id",
    ):
        op.create_index(
            f"ix_dfc_manual_decisions_{column}",
            "dfc_manual_decisions",
            [column],
            unique=False,
        )


def downgrade() -> None:
    for column in (
        "methodology_version_id",
        "entry_number",
        "exercise_id",
        "decision_id",
    ):
        op.drop_index(
            f"ix_dfc_manual_decisions_{column}",
            table_name="dfc_manual_decisions",
        )
    op.drop_table("dfc_manual_decisions")
    for column in (
        "final_status",
        "dfc_component_code",
        "dfc_activity",
        "counterparty_reference_code",
        "counterparty_account_code",
        "entry_number",
        "calculation_id",
    ):
        op.drop_index(f"ix_dfc_audit_rows_{column}", table_name="dfc_audit_rows")
    op.drop_table("dfc_audit_rows")
    for column in (
        "invalidated_at",
        "methodology_version_id",
        "fca_status",
        "exercise_year",
        "analysis_id",
        "exercise_id",
    ):
        op.drop_index(
            f"ix_dfc_calculations_{column}", table_name="dfc_calculations"
        )
    op.drop_table("dfc_calculations")

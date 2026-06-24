"""create declared account snapshots

Revision ID: 0038_declared_account_snapshots
Revises: None
Create Date: 2026-06-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0038_declared_account_snapshots"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "declared_account_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_year", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("account_name", sa.String(length=255), nullable=False),
        sa.Column("declared_reference_code", sa.String(length=64), nullable=True),
        sa.Column("official_description", sa.String(length=255), nullable=True),
        sa.Column("official_reference_status", sa.String(length=80), nullable=True),
        sa.Column("methodology_rule_applied", sa.String(length=64), nullable=True),
        sa.Column("methodology_rule_status", sa.String(length=80), nullable=True),
        sa.Column("purpose", sa.String(length=80), nullable=False),
        sa.Column("base_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("considered_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("final_status", sa.String(length=100), nullable=False),
        sa.Column("observation", sa.String(length=500), nullable=True),
        sa.Column("recommended_action", sa.String(length=120), nullable=True),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_declared_account_snapshots_account_code",
        "declared_account_snapshots",
        ["account_code"],
        unique=False,
    )
    op.create_index(
        "ix_declared_account_snapshots_analysis_id",
        "declared_account_snapshots",
        ["analysis_id"],
        unique=False,
    )
    op.create_index(
        "ix_declared_account_snapshots_exercise_year",
        "declared_account_snapshots",
        ["exercise_year"],
        unique=False,
    )
    op.create_index(
        "ix_declared_account_snapshots_final_status",
        "declared_account_snapshots",
        ["final_status"],
        unique=False,
    )
    op.create_index(
        "ix_declared_account_snapshots_methodology_version_id",
        "declared_account_snapshots",
        ["methodology_version_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_declared_account_snapshots_methodology_version_id",
        table_name="declared_account_snapshots",
    )
    op.drop_index(
        "ix_declared_account_snapshots_final_status",
        table_name="declared_account_snapshots",
    )
    op.drop_index(
        "ix_declared_account_snapshots_exercise_year",
        table_name="declared_account_snapshots",
    )
    op.drop_index(
        "ix_declared_account_snapshots_analysis_id",
        table_name="declared_account_snapshots",
    )
    op.drop_index(
        "ix_declared_account_snapshots_account_code",
        table_name="declared_account_snapshots",
    )
    op.drop_table("declared_account_snapshots")

"""create CAPAG-E assessment snapshots

Revision ID: 0051_capag_assessments
Revises: 0041b_ecd_normalized_tables
Create Date: 2026-07-24
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0051_capag_assessments"
down_revision: Union[str, None] = "0041b_ecd_normalized_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "capag_assessments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("exercise_year", sa.Integer(), nullable=False),
        sa.Column("method", sa.String(length=40), nullable=False),
        sa.Column("plra_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("plra_status", sa.String(length=40), nullable=False),
        sa.Column("fca_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("fca_status", sa.String(length=40), nullable=False),
        sa.Column("roa_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("roa_status", sa.String(length=40), nullable=False),
        sa.Column("capag_e_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("capag_e_status", sa.String(length=40), nullable=False),
        sa.Column("unavailable_reason", sa.Text(), nullable=True),
        sa.Column("calculation_basis", sa.Text(), nullable=False),
        sa.Column("methodology_formula", sa.Text(), nullable=False),
        sa.Column("warnings_json", sa.JSON(), nullable=False),
        sa.Column("limitations_json", sa.JSON(), nullable=False),
        sa.Column("blocking_issues_json", sa.JSON(), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_capag_assessments_capag_e_status",
        "capag_assessments",
        ["capag_e_status"],
        unique=False,
    )
    op.create_index(
        "ix_capag_assessments_exercise_id",
        "capag_assessments",
        ["exercise_id"],
        unique=False,
    )
    op.create_index(
        "ix_capag_assessments_exercise_year",
        "capag_assessments",
        ["exercise_year"],
        unique=False,
    )
    op.create_index(
        "ix_capag_assessments_method",
        "capag_assessments",
        ["method"],
        unique=False,
    )
    op.create_index(
        "ix_capag_assessments_methodology_version_id",
        "capag_assessments",
        ["methodology_version_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_capag_assessments_methodology_version_id",
        table_name="capag_assessments",
    )
    op.drop_index("ix_capag_assessments_method", table_name="capag_assessments")
    op.drop_index(
        "ix_capag_assessments_exercise_year",
        table_name="capag_assessments",
    )
    op.drop_index(
        "ix_capag_assessments_exercise_id",
        table_name="capag_assessments",
    )
    op.drop_index(
        "ix_capag_assessments_capag_e_status",
        table_name="capag_assessments",
    )
    op.drop_table("capag_assessments")

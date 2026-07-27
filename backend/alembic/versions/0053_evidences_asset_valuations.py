"""create evidences and asset valuation assessments

Revision ID: 0053_evidences_assets
Revises: 0052_plra_calculations
Create Date: 2026-07-24
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0053_evidences_assets"
down_revision: Union[str, None] = "0052_plra_calculations"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "plra_calculations",
        sa.Column("invalidated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_plra_calculations_invalidated_at",
        "plra_calculations",
        ["invalidated_at"],
        unique=False,
    )
    op.create_table(
        "adjustment_evidences",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("evidence_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("exercise_year", sa.Integer(), nullable=False),
        sa.Column("scope_type", sa.String(length=40), nullable=False),
        sa.Column("scope_key", sa.String(length=120), nullable=False),
        sa.Column("adjustment_type", sa.String(length=80), nullable=False),
        sa.Column("method_component", sa.String(length=20), nullable=False),
        sa.Column("amount_impact", sa.Numeric(18, 2), nullable=False),
        sa.Column("impact_base_value", sa.Numeric(18, 2), nullable=True),
        sa.Column("impact_percent", sa.Numeric(12, 6), nullable=True),
        sa.Column("materiality_level", sa.String(length=20), nullable=False),
        sa.Column("materiality_source", sa.String(length=30), nullable=False),
        sa.Column(
            "minimum_materiality_level", sa.String(length=20), nullable=False
        ),
        sa.Column("required_evidence_type", sa.String(length=120), nullable=True),
        sa.Column("evidence_status", sa.String(length=50), nullable=False),
        sa.Column("analyst_justification", sa.Text(), nullable=True),
        sa.Column("review_notes", sa.Text(), nullable=True),
        sa.Column("blocks_final_report", sa.Boolean(), nullable=False),
        sa.Column("requires_reservation", sa.Boolean(), nullable=False),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("decision_reasons_json", sa.JSON(), nullable=False),
        sa.Column("materiality_overrides_json", sa.JSON(), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("evidence_id"),
    )
    for column in (
        "evidence_id",
        "exercise_id",
        "exercise_year",
        "scope_type",
        "scope_key",
        "method_component",
        "materiality_level",
        "evidence_status",
        "blocks_final_report",
        "methodology_version_id",
        "updated_at",
    ):
        op.create_index(
            f"ix_adjustment_evidences_{column}",
            "adjustment_evidences",
            [column],
            unique=column == "evidence_id",
        )
    op.create_table(
        "asset_valuation_assessments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("assessment_id", sa.String(length=64), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("exercise_year", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(length=64), nullable=False),
        sa.Column("account_name", sa.String(length=255), nullable=False),
        sa.Column("reference_code", sa.String(length=64), nullable=False),
        sa.Column("macrogroup", sa.String(length=80), nullable=False),
        sa.Column("book_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("default_desagio_percent", sa.Numeric(8, 6), nullable=False),
        sa.Column("default_economic_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("valuation_required", sa.Boolean(), nullable=False),
        sa.Column(
            "realizability_classification", sa.String(length=60), nullable=False
        ),
        sa.Column("valuation_basis", sa.String(length=50), nullable=False),
        sa.Column("forced_liquidation_value", sa.Numeric(18, 2), nullable=True),
        sa.Column("analyst_adjusted_value", sa.Numeric(18, 2), nullable=True),
        sa.Column("final_economic_value", sa.Numeric(18, 2), nullable=False),
        sa.Column("final_value_source", sa.String(length=50), nullable=False),
        sa.Column("essentiality_status", sa.String(length=30), nullable=False),
        sa.Column("evidence_id", sa.String(length=64), nullable=True),
        sa.Column("valuation_status", sa.String(length=30), nullable=False),
        sa.Column("blocks_plra", sa.Boolean(), nullable=False),
        sa.Column("blocking_reasons_json", sa.JSON(), nullable=False),
        sa.Column("methodology_version_id", sa.String(length=120), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(
            ["evidence_id"], ["adjustment_evidences.evidence_id"]
        ),
        sa.ForeignKeyConstraint(["exercise_id"], ["analysis_exercises.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("assessment_id"),
    )
    for column in (
        "assessment_id",
        "exercise_id",
        "exercise_year",
        "account_code",
        "reference_code",
        "evidence_id",
        "valuation_status",
        "blocks_plra",
        "methodology_version_id",
    ):
        op.create_index(
            f"ix_asset_valuation_assessments_{column}",
            "asset_valuation_assessments",
            [column],
            unique=column == "assessment_id",
        )


def downgrade() -> None:
    op.drop_table("asset_valuation_assessments")
    op.drop_table("adjustment_evidences")
    op.drop_index(
        "ix_plra_calculations_invalidated_at",
        table_name="plra_calculations",
    )
    op.drop_column("plra_calculations", "invalidated_at")

"""propagate declared balance status to PLRA and CAPAG-E

Revision ID: 0058_balance_status
Revises: 0057_reimport_status
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0058_balance_status"
down_revision: Union[str, None] = "0057_reimport_status"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "plra_calculations",
        "j100_reconciliation_status",
        new_column_name="balance_status",
        existing_type=sa.String(length=80),
        type_=sa.String(length=40),
        existing_nullable=False,
    )
    op.execute(
        "UPDATE plra_calculations "
        "SET balance_status = 'OBRIGATORIO_AUSENTE'"
    )
    op.add_column(
        "capag_assessments",
        sa.Column(
            "balance_status",
            sa.String(length=40),
            server_default="OBRIGATORIO_AUSENTE",
            nullable=False,
        ),
    )
    op.alter_column("capag_assessments", "balance_status", server_default=None)


def downgrade() -> None:
    op.drop_column("capag_assessments", "balance_status")
    op.execute(
        "UPDATE plra_calculations "
        "SET balance_status = 'nao_disponivel'"
    )
    op.alter_column(
        "plra_calculations",
        "balance_status",
        new_column_name="j100_reconciliation_status",
        existing_type=sa.String(length=40),
        type_=sa.String(length=80),
        existing_nullable=False,
    )

"""mark legacy ECD imports for controlled reimport

Revision ID: 0057_reimport_status
Revises: 0056_balance_declared
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0057_reimport_status"
down_revision: Union[str, None] = "0056_balance_declared"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "ecd_files",
        sa.Column(
            "preparation_status",
            sa.String(length=40),
            server_default="REIMPORTACAO_NECESSARIA",
            nullable=False,
        ),
    )
    op.add_column(
        "ecd_files",
        sa.Column("reprocessing_result", sa.String(length=40), nullable=True),
    )
    op.create_index(
        "ix_ecd_files_preparation_status",
        "ecd_files",
        ["preparation_status"],
        unique=False,
    )
    op.alter_column("ecd_files", "preparation_status", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_ecd_files_preparation_status", table_name="ecd_files")
    op.drop_column("ecd_files", "reprocessing_result")
    op.drop_column("ecd_files", "preparation_status")

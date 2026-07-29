"""mark parser 2.0 imports for controlled reimport

Revision ID: 0059_parser_2_1
Revises: 0058_balance_status
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op


revision: str = "0059_parser_2_1"
down_revision: Union[str, None] = "0058_balance_status"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "UPDATE ecd_files "
        "SET preparation_status = 'REIMPORTACAO_NECESSARIA', "
        "reprocessing_result = NULL "
        "WHERE parser_version = '2.0.0'"
    )


def downgrade() -> None:
    pass

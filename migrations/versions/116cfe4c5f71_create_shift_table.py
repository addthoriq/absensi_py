"""create shift table

Revision ID: 116cfe4c5f71
Revises: e2bbf1ec6cec
Create Date: 2024-08-03 00:38:34.382371

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "116cfe4c5f71"
down_revision: Union[str, None] = "e2bbf1ec6cec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "shift",
        sa.Column("id", sa.Integer()),
        sa.Column("nama_shift", sa.VARCHAR(length=50)),
        sa.Column("jam_mulai_shift", sa.Time()),
        sa.Column("jam_berakhir_shift", sa.Time()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("shift")

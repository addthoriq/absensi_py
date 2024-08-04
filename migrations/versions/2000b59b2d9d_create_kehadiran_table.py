"""create kehadiran table

Revision ID: 2000b59b2d9d
Revises: 116cfe4c5f71
Create Date: 2024-08-03 00:40:48.619057

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2000b59b2d9d"
down_revision: Union[str, None] = "116cfe4c5f71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "kehadiran",
        sa.Column("id", sa.Integer()),
        sa.Column("nama_kehadiran", sa.String(length=50)),
        sa.Column("keterangan", sa.VARCHAR(length=100)),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("kehadiran")

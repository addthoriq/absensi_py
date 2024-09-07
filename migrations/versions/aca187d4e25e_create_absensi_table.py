"""create absensi table

Revision ID: aca187d4e25e
Revises: 2000b59b2d9d
Create Date: 2024-08-03 00:46:02.332736

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aca187d4e25e"
down_revision: Union[str, None] = "2000b59b2d9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "absensi",
        sa.Column("id", sa.Integer()),
        sa.Column("tanggal_absen", sa.Date()),
        sa.Column("jam_absen_masuk", sa.Time()),
        sa.Column("jam_absen_keluar", sa.Time()),
        sa.Column("keterangan", sa.String(length=100)),
        sa.Column("lokasi", sa.String()),
        sa.Column("user_id", sa.Integer()),
        sa.Column("shift_id", sa.Integer()),
        sa.Column("kehadiran_id", sa.Integer()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["shift_id"], ["shift.id"]),
        sa.ForeignKeyConstraint(["kehadiran_id"], ["kehadiran.id"]),
    )


def downgrade() -> None:
    op.drop_table("absensi")

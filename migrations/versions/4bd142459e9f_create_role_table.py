"""create role table

Revision ID: 4bd142459e9f
Revises: 23fcf284d829
Create Date: 2024-08-03 00:32:17.857424

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4bd142459e9f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "role",
        sa.Column("id", sa.Integer()),
        sa.Column("nama_role", sa.String(length=100)),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("role")

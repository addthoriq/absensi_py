"""create users table

Revision ID: 23fcf284d829
Revises:
Create Date: 2024-07-26 15:40:12.484455

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "23fcf284d829"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer()),
        sa.Column("email", sa.VARCHAR(30), nullable=False),
        sa.Column("nama", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("is_teacher", sa.Boolean(), default=True),
        sa.Column("is_superadmin", sa.Boolean(), default=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")

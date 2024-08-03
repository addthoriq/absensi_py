"""create user table

Revision ID: e2bbf1ec6cec
Revises: 4bd142459e9f
Create Date: 2024-08-03 00:34:39.397124

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e2bbf1ec6cec"
down_revision: Union[str, None] = "4bd142459e9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer()),
        sa.Column("email", sa.VARCHAR(30), nullable=False),
        sa.Column("nama", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Integer()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"]),
    )


def downgrade() -> None:
    op.drop_table("user")

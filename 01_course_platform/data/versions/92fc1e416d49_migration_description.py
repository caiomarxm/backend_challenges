"""{migration_description}

Revision ID: 92fc1e416d49
Revises:
Create Date: 2025-06-03 20:30:05.890714

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "92fc1e416d49"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(500), nullable=False, index=True, unique=True),
        sa.Column("full_name", sa.String(800), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")

"""Create users table

Revision ID: 4cdd351f94c6
Revises: 
Create Date: 2025-06-07 11:18:58.607213

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '4cdd351f94c6'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""

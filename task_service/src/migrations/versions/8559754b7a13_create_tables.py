"""Create tables

Revision ID: 8559754b7a13
Revises: 4cdd351f94c6
Create Date: 2025-06-07 11:29:22.758489

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '8559754b7a13'
down_revision: str | None = '4cdd351f94c6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""

"""Rename user date columns to match models

Revision ID: 6e48a7556c39
Revises: 6e48a7556c38
Create Date: 2025-12-25 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6e48a7556c39'
down_revision: Union[str, None] = '6e48a7556c38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the user table columns from old names to new names
    # created_date -> created_at
    # updated_date -> updated_at
    # Note: In PostgreSQL, we use ALTER TABLE ... RENAME COLUMN
    op.execute("ALTER TABLE \"user\" RENAME COLUMN created_date TO created_at;")
    op.execute("ALTER TABLE \"user\" RENAME COLUMN updated_date TO updated_at;")


def downgrade() -> None:
    # Reverse the column renames
    op.execute("ALTER TABLE \"user\" RENAME COLUMN created_at TO created_date;")
    op.execute("ALTER TABLE \"user\" RENAME COLUMN updated_at TO updated_date;")
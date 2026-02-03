"""Increase message content length from 500 to 2000 characters

Revision ID: 6e48a7556c40
Revises: 6e48a7556c39
Create Date: 2026-01-11 03:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e48a7556c40'
down_revision: Union[str, None] = '6e48a7556c39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter the message content column to allow longer text
    op.alter_column('message', 'content',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.VARCHAR(length=2000),
               existing_nullable=False)


def downgrade() -> None:
    # Downgrade: revert to original length
    op.alter_column('message', 'content',
               existing_type=sa.VARCHAR(length=2000),
               type_=sa.VARCHAR(length=500),
               existing_nullable=False)
"""add content column to table

Revision ID: 012fc473339a
Revises: aa79f0463d2f
Create Date: 2023-10-10 14:40:39.455475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '012fc473339a'
down_revision: Union[str, None] = 'aa79f0463d2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

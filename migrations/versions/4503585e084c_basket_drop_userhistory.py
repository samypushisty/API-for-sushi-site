"""Basket drop UserHistory

Revision ID: 4503585e084c
Revises: 70297441d561
Create Date: 2024-09-30 15:07:52.363406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4503585e084c'
down_revision: Union[str, None] = '70297441d561'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_history')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_history',
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('list_food', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('list_set', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('total_price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('date', name='users_history_pkey')
    )
    # ### end Alembic commands ###

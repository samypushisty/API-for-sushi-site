"""history

Revision ID: 23d67115d520
Revises: e40f3bec32cc
Create Date: 2024-09-27 20:46:03.088717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23d67115d520'
down_revision: Union[str, None] = 'e40f3bec32cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_history_food',
    sa.Column('date', sa.TIMESTAMP(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('food_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('date')
    )
    op.create_table('users_history_set',
    sa.Column('date', sa.TIMESTAMP(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('set_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['set_id'], ['set.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('date')
    )
    op.drop_table('users_history')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_history',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('food_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], name='users_history_food_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='users_history_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_history_pkey')
    )
    op.drop_table('users_history_set')
    op.drop_table('users_history_food')
    # ### end Alembic commands ###

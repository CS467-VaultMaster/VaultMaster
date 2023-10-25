"""Typo

Revision ID: 74415c140e17
Revises: ddc4370000c9
Create Date: 2023-10-24 22:37:22.141801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74415c140e17'
down_revision: Union[str, None] = 'ddc4370000c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('site_user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('last_verified', sa.DateTime(), nullable=True),
    sa.Column('last_login_attempt', sa.DateTime(), nullable=True),
    sa.Column('login_attempts', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('vault',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('vault_name', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('open_attempts', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['site_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('credential',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('nickname', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('node', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('vault_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['vault_id'], ['vault.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('items')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='items_pkey')
    )
    op.drop_table('credential')
    op.drop_table('vault')
    op.drop_table('site_user')
    # ### end Alembic commands ###

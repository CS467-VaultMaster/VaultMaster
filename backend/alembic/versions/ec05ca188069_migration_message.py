"""Migration message

Revision ID: ec05ca188069
Revises: a8e95bc3200b
Create Date: 2023-11-11 01:57:07.163302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec05ca188069'
down_revision: Union[str, None] = 'a8e95bc3200b'
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
    sa.Column('otp_secret', sa.String(), nullable=False),
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
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('fernet_key', sa.String(), nullable=False),
    sa.Column('vault_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['vault_id'], ['vault.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('credential')
    op.drop_table('vault')
    op.drop_table('site_user')
    # ### end Alembic commands ###

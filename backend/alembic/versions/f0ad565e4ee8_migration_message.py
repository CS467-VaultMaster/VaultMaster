"""Migration message

Revision ID: f0ad565e4ee8
Revises: 4210c2d84145
Create Date: 2023-11-03 20:07:00.042187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0ad565e4ee8'
down_revision: Union[str, None] = '4210c2d84145'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('credential', 'fernet_key')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('credential', sa.Column('fernet_key', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

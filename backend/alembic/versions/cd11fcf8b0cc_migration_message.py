"""Migration message

Revision ID: cd11fcf8b0cc
Revises: 3da21cf9b16f
Create Date: 2023-11-10 19:58:55.562091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd11fcf8b0cc'
down_revision: Union[str, None] = '3da21cf9b16f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
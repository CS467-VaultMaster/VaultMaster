"""Migration message

Revision ID: 52c0332cf1b2
Revises: ba66f5ce2f00
Create Date: 2023-11-11 17:29:13.555304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52c0332cf1b2'
down_revision: Union[str, None] = 'ba66f5ce2f00'
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
"""Migration message

Revision ID: 076a6bb22ae6
Revises: 9af7e0ae3b0c
Create Date: 2023-11-11 17:49:03.642449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '076a6bb22ae6'
down_revision: Union[str, None] = '9af7e0ae3b0c'
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
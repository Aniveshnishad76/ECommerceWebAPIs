"""first name and last name added

Revision ID: 7ac1ac3e78cd
Revises: e85114a6d76e
Create Date: 2025-01-22 18:31:00.706045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ac1ac3e78cd'
down_revision: Union[str, None] = 'e85114a6d76e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.VARCHAR(length=100), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.VARCHAR(length=100), nullable=True))
    op.execute(
        """UPDATE public.user
        SET first_name = 'Anivesh',
            last_name = 'Nishad'
        """
    )
    op.drop_column('user', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
    op.execute(
        """
        UPDATE public.user
        SET name = first_name || ' ' || last_name
        """
    )
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###

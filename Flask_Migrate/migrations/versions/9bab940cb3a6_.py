"""empty message

Revision ID: 9bab940cb3a6
Revises: 1cf9c7d938b0
Create Date: 2023-03-23 12:30:41.587476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bab940cb3a6'
down_revision = '1cf9c7d938b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'description')
    # ### end Alembic commands ###

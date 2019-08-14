"""empty message

Revision ID: 2affb78c8689
Revises: bba98862e706
Create Date: 2019-07-01 10:13:49.223033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2affb78c8689'
down_revision = 'bba98862e706'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donations', sa.Column('approved', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('donations', 'approved')
    # ### end Alembic commands ###

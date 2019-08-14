"""create donations table

Revision ID: 130f38c48710
Revises:
Create Date: 2019-06-10 13:01:19.017570

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '130f38c48710'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('donations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('raw_donation', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('donated_at', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('vod_youtube_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('vod_published_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='donations_pkey')
    )

def downgrade():
    op.drop_table('donations')

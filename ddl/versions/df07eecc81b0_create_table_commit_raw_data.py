"""create table commit_raw_data

Revision ID: df07eecc81b0
Revises: 
Create Date: 2019-09-27 16:05:06.368645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df07eecc81b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'git_raw_data',
    sa.Column('node_id',sa.String(length=100), primary_key=True),
    sa.Column('html_url', sa.String(length=100), nullable=True),
    sa.Column('comments_url', sa.String(length=100), nullable=True),
    sa.Column('commit', sa.String(length=1024), nullable=True),
    sa.Column('parents',  sa.String(length=512), nullable=True),
    sa.Column('sha', sa.String(length=100), nullable=True),
    sa.Column('author', sa.String(length=1024), nullable=True),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.Column('committer', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('node_id') 
    )

def downgrade():
    op.drop_table('git_raw_data')

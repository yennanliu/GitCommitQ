"""create table commit_raw

Revision ID: e236a01e6be0
Revises: df07eecc81b0
Create Date: 2019-09-27 16:31:23.513385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e236a01e6be0'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
    'raw_git_commit',
    sa.Column('node_id',sa.String(length=256), primary_key=True),
    sa.Column('html_url', sa.String(length=256), nullable=True),
    sa.Column('comments_url',  sa.UnicodeText(), nullable=True),
    sa.Column('commit', sa.UnicodeText(), nullable=True),
    sa.Column('parents',  sa.String(length=512), nullable=True),
    sa.Column('sha', sa.String(length=256), nullable=True),
    sa.Column('author',  sa.UnicodeText(), nullable=True),
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.Column('committer', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('node_id') 
    )

def downgrade():
    op.drop_table('raw_git_commit')

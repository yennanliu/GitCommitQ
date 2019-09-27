"""create table commit

Revision ID: b6e38d643ecd
Revises: e236a01e6be0
Create Date: 2019-09-27 23:44:11.011620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6e38d643ecd'
down_revision = 'e236a01e6be0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'git_commit',
    sa.Column('user_id',sa.String(length=256)),
    sa.Column('commit_url', sa.String(length=256), primary_key=True),
    sa.Column('repo_url',  sa.String(length=256), nullable=True),
    sa.Column('commit_timestamp',  sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('commit_url') 
    )

def downgrade():
    op.drop_table('git_commit')

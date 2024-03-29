"""empty message

Revision ID: 24eb5d9ee4dc
Revises: 14a0fa4c9971
Create Date: 2015-07-06 11:13:46.177285

"""

# revision identifiers, used by Alembic.
revision = '24eb5d9ee4dc'
down_revision = '14a0fa4c9971'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('title', sa.String(length=255), nullable=True))
    op.create_index('ix_posts_title', 'posts', ['title'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_title', 'posts')
    op.drop_column('posts', 'title')
    ### end Alembic commands ###

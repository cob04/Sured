"""empty message

Revision ID: 1172e0a1cdb
Revises: 7c77df778d5
Create Date: 2015-06-30 15:42:13.774323

"""

# revision identifiers, used by Alembic.
revision = '1172e0a1cdb'
down_revision = '7c77df778d5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_creations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_creations')
    ### end Alembic commands ###
"""empty message

Revision ID: d5c01baa9a7
Revises: 8c9ee68e96f
Create Date: 2015-06-28 10:35:38.779114

"""

# revision identifiers, used by Alembic.
revision = 'd5c01baa9a7'
down_revision = '8c9ee68e96f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_questions_timestamp', 'questions', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_questions_timestamp', 'questions')
    op.drop_table('questions')
    ### end Alembic commands ###
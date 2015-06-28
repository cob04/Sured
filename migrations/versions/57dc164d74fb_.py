"""empty message

Revision ID: 57dc164d74fb
Revises: 2466abc753ac
Create Date: 2015-06-28 17:32:31.218465

"""

# revision identifiers, used by Alembic.
revision = '57dc164d74fb'
down_revision = '2466abc753ac'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_posts_timestamp', 'posts', ['timestamp'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_comments_timestamp', 'comments', ['timestamp'], unique=False)
    op.drop_table(u'answers')
    op.drop_table(u'questions')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'questions',
    sa.Column(u'id', sa.INTEGER(), nullable=False),
    sa.Column(u'body', sa.TEXT(), nullable=True),
    sa.Column(u'timestamp', sa.DATETIME(), nullable=True),
    sa.Column(u'author_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], [u'users.id'], ),
    sa.PrimaryKeyConstraint(u'id')
    )
    op.create_table(u'answers',
    sa.Column(u'id', sa.INTEGER(), nullable=False),
    sa.Column(u'body', sa.TEXT(), nullable=True),
    sa.Column(u'timestamp', sa.DATETIME(), nullable=True),
    sa.Column(u'disabled', sa.BOOLEAN(), nullable=True),
    sa.Column(u'author_id', sa.INTEGER(), nullable=True),
    sa.Column(u'question_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], [u'users.id'], ),
    sa.ForeignKeyConstraint(['question_id'], [u'questions.id'], ),
    sa.PrimaryKeyConstraint(u'id')
    )
    op.drop_index('ix_comments_timestamp', 'comments')
    op.drop_table('comments')
    op.drop_index('ix_posts_timestamp', 'posts')
    op.drop_table('posts')
    ### end Alembic commands ###
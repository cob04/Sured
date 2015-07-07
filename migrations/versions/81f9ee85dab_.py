"""empty message

Revision ID: 81f9ee85dab
Revises: None
Create Date: 2015-07-07 09:05:10.228863

"""

# revision identifiers, used by Alembic.
revision = '81f9ee85dab'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_creations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_creations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index('ix_roles_default', 'roles', ['default'], unique=False)
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tags_name', 'tags', ['name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_posts_timestamp', 'posts', ['timestamp'], unique=False)
    op.create_index('ix_posts_title', 'posts', ['title'], unique=False)
    op.create_table('follows',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('answer', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_comments_timestamp', 'comments', ['timestamp'], unique=False)
    op.create_table('tagged',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tagged')
    op.drop_index('ix_comments_timestamp', 'comments')
    op.drop_table('comments')
    op.drop_table('follows')
    op.drop_index('ix_posts_title', 'posts')
    op.drop_index('ix_posts_timestamp', 'posts')
    op.drop_table('posts')
    op.drop_index('ix_users_username', 'users')
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
    op.drop_index('ix_tags_name', 'tags')
    op.drop_table('tags')
    op.drop_index('ix_roles_default', 'roles')
    op.drop_table('roles')
    op.drop_table('post_creations')
    op.drop_table('account_creations')
    ### end Alembic commands ###
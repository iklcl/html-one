"""empty message

Revision ID: 359e7b6adfc0
Revises: 
Create Date: 2018-05-09 14:05:34.379000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359e7b6adfc0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('telephone', sa.String(length=11), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('nub', sa.INTEGER(), nullable=False),
    sa.Column('beizhu', sa.Text(), nullable=True),
    sa.Column('zhuangtai', sa.String(length=100), nullable=True),
    sa.Column('filename', sa.String(length=100), nullable=True),
    sa.Column('data_name', sa.String(length=100), nullable=True),
    sa.Column('custom', sa.String(length=100), nullable=True),
    sa.Column('svnUrl', sa.String(length=100), nullable=True),
    sa.Column('progress', sa.String(length=100), nullable=True),
    sa.Column('task', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('content', sa.String(length=100), nullable=False),
    sa.Column('filename_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['filename_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    op.drop_table('question')
    op.drop_table('user')
    # ### end Alembic commands ###

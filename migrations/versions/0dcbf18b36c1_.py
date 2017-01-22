"""empty message

Revision ID: 0dcbf18b36c1
Revises: 
Create Date: 2017-01-22 16:24:52.582837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dcbf18b36c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.add_column('entry', sa.Column('rating', sa.Integer(), nullable=True))
    op.add_column('entry', sa.Column('response_time', sa.Integer(), nullable=True))
    op.add_column('entry', sa.Column('review', sa.Integer(), nullable=True))
    op.add_column('profile_analysis', sa.Column('entry_url', sa.Integer(), nullable=True))
    op.drop_constraint('profile_analysis_user_id_fkey', 'profile_analysis', type_='foreignkey')
    op.create_foreign_key(None, 'profile_analysis', 'entry', ['entry_url'], ['url'])
    op.drop_column('profile_analysis', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile_analysis', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'profile_analysis', type_='foreignkey')
    op.create_foreign_key('profile_analysis_user_id_fkey', 'profile_analysis', 'user', ['user_id'], ['id'])
    op.drop_column('profile_analysis', 'entry_url')
    op.drop_column('entry', 'review')
    op.drop_column('entry', 'response_time')
    op.drop_column('entry', 'rating')
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('review', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('response_time', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    # ### end Alembic commands ###

"""empty message

Revision ID: 27d0031ef9f6
Revises: 
Create Date: 2020-08-29 23:58:13.758452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27d0031ef9f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('dashboards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('dashboards_mtm',
    sa.Column('dashboards_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dashboards_id'], ['dashboards.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('dashboards_id', 'users_id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('dashboard_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['dashboard_id'], ['dashboards.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tasks_mtm',
    sa.Column('tasks_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tasks_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('tasks_id', 'users_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks_mtm')
    op.drop_table('tasks')
    op.drop_table('dashboards_mtm')
    op.drop_table('dashboards')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
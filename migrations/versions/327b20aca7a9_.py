"""empty message

Revision ID: 327b20aca7a9
Revises: 80644df0bd0a
Create Date: 2024-09-25 11:42:51.824491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '327b20aca7a9'
down_revision = '80644df0bd0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'company', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('cost', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'cost', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('transport', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'transport', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transport', type_='foreignkey')
    op.drop_column('transport', 'user_id')
    op.drop_constraint(None, 'cost', type_='foreignkey')
    op.drop_column('cost', 'user_id')
    op.drop_constraint(None, 'company', type_='foreignkey')
    op.drop_column('company', 'user_id')

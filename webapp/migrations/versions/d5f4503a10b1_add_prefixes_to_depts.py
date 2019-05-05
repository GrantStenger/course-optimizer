"""add prefixes to depts

Revision ID: d5f4503a10b1
Revises: 59e5320f741c
Create Date: 2019-05-04 17:05:17.892699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5f4503a10b1'
down_revision = '59e5320f741c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('department', sa.Column('prefix', sa.String(length=4)))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('department', 'prefix')
    # ### end Alembic commands ###

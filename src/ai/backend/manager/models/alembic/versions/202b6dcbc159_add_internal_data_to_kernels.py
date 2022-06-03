"""add-internal-data-to-kernels

Revision ID: 202b6dcbc159
Revises: 3f1dafab60b2
Create Date: 2019-10-01 16:13:20.935285

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '202b6dcbc159'
down_revision = '3f1dafab60b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kernels', sa.Column('internal_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('kernels', 'internal_data')
    # ### end Alembic commands ###

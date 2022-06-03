"""keypairs_get_is_admin

Revision ID: 80176413d8aa
Revises: 4b8a66fb8d82
Create Date: 2017-09-14 16:01:59.994941

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import false

# revision identifiers, used by Alembic.
revision = '80176413d8aa'
down_revision = '4b8a66fb8d82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('keypairs', sa.Column('is_admin', sa.Boolean(), nullable=False, default=False, server_default=false()))
    op.create_index(op.f('ix_keypairs_is_admin'), 'keypairs', ['is_admin'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_keypairs_is_admin'), table_name='keypairs')
    op.drop_column('keypairs', 'is_admin')
    # ### end Alembic commands ###

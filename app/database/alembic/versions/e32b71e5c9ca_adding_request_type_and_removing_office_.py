"""adding request type and removing office, zone and delegation to social case table

Revision ID: e32b71e5c9ca
Revises: e8aa52cc082e
Create Date: 2022-01-19 16:09:44.692179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e32b71e5c9ca'
down_revision = 'e8aa52cc082e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('social_case', sa.Column('request_type', sa.String(length=400), server_default='Tipo de solicitud', nullable=False))
    op.drop_column('social_case', 'office')
    op.drop_column('social_case', 'delegation')
    op.drop_column('social_case', 'zone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('social_case', sa.Column('zone', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('social_case', sa.Column('delegation', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.add_column('social_case', sa.Column('office', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.drop_column('social_case', 'request_type')
    # ### end Alembic commands ###

"""adding intervention plan table

Revision ID: af570eb9b821
Revises: 63af805e04c1
Create Date: 2021-12-09 16:48:52.802607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af570eb9b821'
down_revision = '63af805e04c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('intervention_plan',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('next_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('frequency', sa.String(length=15), nullable=False),
    sa.Column('social_case_id', sa.Integer(), nullable=False),
    sa.Column('management_id', sa.Integer(), nullable=False),
    sa.Column('management_name', sa.String(length=120), nullable=False),
    sa.Column('professional_id', sa.Integer(), nullable=False),
    sa.Column('professional_names', sa.String(length=200), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('update_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['social_case_id'], ['social_case.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'social_case', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'social_case', type_='unique')
    op.drop_table('intervention_plan')
    # ### end Alembic commands ###

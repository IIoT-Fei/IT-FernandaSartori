"""empty message

Revision ID: d5f5481feeee
Revises: 6f9566bc355c
Create Date: 2018-02-02 17:18:47.097840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5f5481feeee'
down_revision = '6f9566bc355c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('disciplina', sa.Column('id_prof', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('disciplina', 'id_prof')
    # ### end Alembic commands ###
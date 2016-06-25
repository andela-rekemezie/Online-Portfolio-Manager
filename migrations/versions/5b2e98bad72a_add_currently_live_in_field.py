"""Add currently live in field

Revision ID: 5b2e98bad72a
Revises: 
Create Date: 2016-06-25 19:54:23.030100

"""

# revision identifiers, used by Alembic.
revision = '5b2e98bad72a'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('currently_live_in', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'currently_live_in')
    ### end Alembic commands ###

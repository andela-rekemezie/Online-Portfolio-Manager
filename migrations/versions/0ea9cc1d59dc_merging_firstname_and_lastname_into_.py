"""Merging firstname and lastname into fullname

Revision ID: 0ea9cc1d59dc
Revises: 5b2e98bad72a
Create Date: 2016-06-25 20:35:22.647563

"""

# revision identifiers, used by Alembic.
revision = '0ea9cc1d59dc'
down_revision = '5b2e98bad72a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    print "Adding fullname column"
    op.add_column('users', sa.Column('fullname', sa.String(30)))

    print "Merging firstname and lastname into fullname"
    connection = op.get_bind()
    connection.execute("update users set fullname = subquery.newfullname from (select id, concat(firstname, ' ', lastname)  as newfullname from users) as subquery where users.id = subquery.id", execute_options=None)

    print "Dropping firstname and lastname field"
    op.drop_column('users', 'firstname')
    op.drop_column('users', 'lastname')


def downgrade():
    connection = op.get_bind()
    op.add_column('users', sa.Column('firstname', sa.String(101)))
    op.add_column('users', sa.Column('lastname', sa.String(102)))
    connection.execute('update users set firstname = fullname')

    print "Drop fullname field"
    op.drop_column('users', 'fullname')

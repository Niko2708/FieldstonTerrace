"""empty message

Revision ID: ca1b50e3bf0d
Revises: 0e08b7e79076
Create Date: 2020-10-20 12:02:33.170877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca1b50e3bf0d'
down_revision = '0e08b7e79076'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('name')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=60), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('name')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=60), nullable=True))

    # ### end Alembic commands ###

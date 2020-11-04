"""Added start and end time

Revision ID: 08d358f18f59
Revises: 2c641bc6f22d
Create Date: 2020-11-02 14:20:04.590243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08d358f18f59'
down_revision = '2c641bc6f22d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('end', sa.Time(), nullable=True))
        batch_op.add_column(sa.Column('start', sa.Time(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('start')
        batch_op.drop_column('end')

    # ### end Alembic commands ###
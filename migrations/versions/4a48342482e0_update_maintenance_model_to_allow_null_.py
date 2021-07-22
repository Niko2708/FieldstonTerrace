"""Update Maintenance model to allow null option for imgs

Revision ID: 4a48342482e0
Revises: a965050cb096
Create Date: 2021-07-12 12:54:28.446860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a48342482e0'
down_revision = 'a965050cb096'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('maintenance', schema=None) as batch_op:
        batch_op.alter_column('maintenance_img',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('maintenance', schema=None) as batch_op:
        batch_op.alter_column('maintenance_img',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)

    # ### end Alembic commands ###

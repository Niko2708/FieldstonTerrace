"""add author col in Post

Revision ID: 4671802a08fb
Revises: ca1b50e3bf0d
Create Date: 2020-10-20 12:05:30.012633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4671802a08fb'
down_revision = 'ca1b50e3bf0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.String(length=60), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('author')

    # ### end Alembic commands ###

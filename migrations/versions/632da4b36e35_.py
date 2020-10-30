"""empty message

Revision ID: 632da4b36e35
Revises: cf6600984258
Create Date: 2020-09-18 20:51:28.011505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '632da4b36e35'
down_revision = 'cf6600984258'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('facebook', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('google', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'google')
    op.drop_column('users', 'facebook')
    # ### end Alembic commands ###

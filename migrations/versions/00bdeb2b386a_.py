"""empty message

Revision ID: 00bdeb2b386a
Revises: 
Create Date: 2021-08-11 15:52:38.705684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00bdeb2b386a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('summary', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news')
    # ### end Alembic commands ###

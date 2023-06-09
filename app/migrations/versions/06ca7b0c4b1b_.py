"""empty message

Revision ID: 06ca7b0c4b1b
Revises: 
Create Date: 2023-03-12 01:06:09.189097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06ca7b0c4b1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('captain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=50), nullable=True),
    sa.Column('lastname', sa.String(length=50), nullable=True),
    sa.Column('rank', sa.String(length=50), nullable=True),
    sa.Column('homeplanet', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spaceship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('maxweight', sa.Float(), nullable=True),
    sa.Column('captainid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['captainid'], ['captain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cargo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('cargotype', sa.String(length=50), nullable=True),
    sa.Column('departure', sa.Date(), nullable=True),
    sa.Column('arrival', sa.Date(), nullable=True),
    sa.Column('shipid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shipid'], ['spaceship.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cargo')
    op.drop_table('spaceship')
    op.drop_table('captain')
    # ### end Alembic commands ###

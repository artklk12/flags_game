"""10 rounds

Revision ID: 7391f2a66e89
Revises: 8dff44dd3c3e
Create Date: 2023-02-12 16:40:40.866456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7391f2a66e89'
down_revision = '8dff44dd3c3e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('matches', sa.Column('round6', sa.String(), nullable=True))
    op.add_column('matches', sa.Column('round7', sa.String(), nullable=True))
    op.add_column('matches', sa.Column('round8', sa.String(), nullable=True))
    op.add_column('matches', sa.Column('round9', sa.String(), nullable=True))
    op.add_column('matches', sa.Column('round10', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('matches', 'round10')
    op.drop_column('matches', 'round9')
    op.drop_column('matches', 'round8')
    op.drop_column('matches', 'round7')
    op.drop_column('matches', 'round6')
    # ### end Alembic commands ###

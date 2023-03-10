"""alter name rounds2

Revision ID: 10fe85277cfd
Revises: e654dd267ff9
Create Date: 2023-02-11 20:01:19.899621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10fe85277cfd'
down_revision = 'e654dd267ff9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('matches_rounds', sa.Column('match_id', sa.Integer(), nullable=True))
    op.drop_constraint('matches_rounds_match_fkey', 'matches_rounds', type_='foreignkey')
    op.create_foreign_key(None, 'matches_rounds', 'matches', ['match_id'], ['id'])
    op.drop_column('matches_rounds', 'match')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('matches_rounds', sa.Column('match', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'matches_rounds', type_='foreignkey')
    op.create_foreign_key('matches_rounds_match_fkey', 'matches_rounds', 'matches', ['match'], ['id'])
    op.drop_column('matches_rounds', 'match_id')
    # ### end Alembic commands ###

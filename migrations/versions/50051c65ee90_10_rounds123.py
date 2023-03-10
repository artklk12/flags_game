"""10 rounds123

Revision ID: 50051c65ee90
Revises: 7391f2a66e89
Create Date: 2023-02-14 02:20:20.131052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50051c65ee90'
down_revision = '7391f2a66e89'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flags_cards',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('title')
    )
    op.create_index(op.f('ix_flags_cards_title'), 'flags_cards', ['title'], unique=True)
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player1', sa.BigInteger(), nullable=True),
    sa.Column('player2', sa.BigInteger(), nullable=True),
    sa.Column('round1', sa.String(), nullable=True),
    sa.Column('round2', sa.String(), nullable=True),
    sa.Column('round3', sa.String(), nullable=True),
    sa.Column('round4', sa.String(), nullable=True),
    sa.Column('round5', sa.String(), nullable=True),
    sa.Column('round6', sa.String(), nullable=True),
    sa.Column('round7', sa.String(), nullable=True),
    sa.Column('round8', sa.String(), nullable=True),
    sa.Column('round9', sa.String(), nullable=True),
    sa.Column('round10', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_matches_id'), 'matches', ['id'], unique=True)
    op.create_table('matches_rounds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.BigInteger(), nullable=True),
    sa.Column('round', sa.Integer(), nullable=True),
    sa.Column('player_answer', sa.String(), nullable=True),
    sa.Column('correct_answer', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_matches_rounds_id'), 'matches_rounds', ['id'], unique=True)
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.drop_index(op.f('ix_matches_rounds_id'), table_name='matches_rounds')
    op.drop_table('matches_rounds')
    op.drop_index(op.f('ix_matches_id'), table_name='matches')
    op.drop_table('matches')
    op.drop_index(op.f('ix_flags_cards_title'), table_name='flags_cards')
    op.drop_table('flags_cards')
    # ### end Alembic commands ###

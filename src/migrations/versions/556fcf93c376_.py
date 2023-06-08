"""empty message

Revision ID: 556fcf93c376
Revises: 
Create Date: 2023-06-08 23:43:12.602792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '556fcf93c376'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('review_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('bin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_review_type_id', sa.Integer(), nullable=False),
    sa.Column('to_review_type_id', sa.Integer(), nullable=False),
    sa.Column('time_delay_hours', sa.Integer(), nullable=False),
    sa.Column('incorrect_answer_decrementer', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['from_review_type_id'], ['review_type.id'], ),
    sa.ForeignKeyConstraint(['to_review_type_id'], ['review_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bin_id', sa.Integer(), nullable=False),
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('next_review', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['bin_id'], ['bin.id'], ),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('vocabulary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vocabulary')
    op.drop_table('card')
    op.drop_table('bin')
    op.drop_table('review_type')
    op.drop_table('deck')
    # ### end Alembic commands ###
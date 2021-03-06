"""words model

Revision ID: 5a51406c432f
Revises: 8cc3167edd35
Create Date: 2019-01-31 17:15:18.169889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a51406c432f'
down_revision = '8cc3167edd35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('word',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=150), nullable=True),
    sa.Column('translate', sa.String(length=150), nullable=True),
    sa.Column('sentence', sa.String(length=300), nullable=True),
    sa.Column('comment', sa.String(length=300), nullable=True),
    sa.Column('repeat_count', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_word_word'), 'word', ['word'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_word_word'), table_name='word')
    op.drop_table('word')
    # ### end Alembic commands ###

"""update

Revision ID: dbfa1e62dda7
Revises: 849f9f7583b2
Create Date: 2023-09-23 21:53:28.481941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbfa1e62dda7'
down_revision = '849f9f7583b2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_table('articles',
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('color', sa.Enum('RED', 'GREEN', 'BLUE', name='colorenum'), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name=op.f('fk_articles_author_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_articles'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('articles')
    op.drop_table('users')
    # ### end Alembic commands ###
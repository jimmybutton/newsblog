"""Article created and updated

Revision ID: d56e673cefc2
Revises: 5526cbe78d8f
Create Date: 2019-12-06 23:22:24.613527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd56e673cefc2'
down_revision = '5526cbe78d8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('article', sa.Column('updated', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_article_created'), 'article', ['created'], unique=False)
    op.create_index(op.f('ix_article_updated'), 'article', ['updated'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_article_updated'), table_name='article')
    op.drop_index(op.f('ix_article_created'), table_name='article')
    op.drop_column('article', 'updated')
    op.drop_column('article', 'created')
    # ### end Alembic commands ###
"""add author to notes

Revision ID: add_author_to_notes
Revises: add_users
Create Date: 2024-04-18 21:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_author_to_notes'
down_revision = 'add_users'
branch_labels = None
depends_on = None

def upgrade():
    # Add author column to notes table
    op.add_column('notes', sa.Column('author', sa.Text(), nullable=True))

def downgrade():
    # Remove author column from notes table
    op.drop_column('notes', 'author') 
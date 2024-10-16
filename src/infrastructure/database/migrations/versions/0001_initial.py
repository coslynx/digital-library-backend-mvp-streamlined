from alembic import op
import sqlalchemy as sa

# Import the Book and User models from the database models
from src.infrastructure.database.models.book import Book
from src.infrastructure.database.models.user import User

def upgrade():
    """
    This function is called by Alembic to apply the migration.

    It creates the initial tables for the Book and User models.
    """
    op.create_table('books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('isbn', sa.String(), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('publication_date', sa.DateTime()),
        sa.Column('language', sa.String()),
        sa.Column('genre', sa.String()),
        sa.Column('cover_image', sa.String()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False, default='patron'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    """
    This function is called by Alembic to revert the migration.

    It drops the Book and User tables.
    """
    op.drop_table('users')
    op.drop_table('books')
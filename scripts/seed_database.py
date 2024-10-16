from sqlalchemy.orm import Session
from src.infrastructure.database.engine import engine
from src.infrastructure.database.models.base import Base
from src.domain.books.models.book import Book
from src.domain.users.models.user import User
from src.utils.exceptions import DatabaseError
from src.utils.logger import Logger
from src.config.settings import settings

logger = Logger(__name__)

def seed_database(session: Session):
    """Seeds the database with initial data."""
    try:
        logger.info("Seeding database with initial data...")

        # Seed users
        staff_user = User(username="staff", email="staff@example.com", password_hash=User.set_password("password"), role="staff")
        patron_user = User(username="patron", email="patron@example.com", password_hash=User.set_password("password"), role="patron")

        session.add(staff_user)
        session.add(patron_user)
        session.commit()

        # Seed books
        book1 = Book(
            title="The Hitchhiker's Guide to the Galaxy",
            author="Douglas Adams",
            isbn="9780345391803",
            description="A humorous science fiction novel about a man who is unexpectedly forced to leave Earth just before it is destroyed to make way for a hyperspace bypass.",
            publication_date="1979-10-12",
            language="English",
            genre="Science Fiction",
        )

        book2 = Book(
            title="Pride and Prejudice",
            author="Jane Austen",
            isbn="9780141439518",
            description="A classic romantic novel set in England in the late 18th century, focusing on the Bennet sisters and their search for love and marriage.",
            publication_date="1813-01-28",
            language="English",
            genre="Romance",
        )

        session.add(book1)
        session.add(book2)
        session.commit()

        logger.info("Database seeded successfully!")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise DatabaseError(f"Error seeding database: {e}")

if __name__ == "__main__":
    logger.info("Starting database seeding process...")
    Base.metadata.create_all(bind=engine)  # Ensure tables exist
    with Session(engine) as session:
        seed_database(session)
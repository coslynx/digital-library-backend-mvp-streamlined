from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.book import Book
from src.infrastructure.database.models.user import User
from src.config.settings import settings
from src.utils.logger import Logger

logger = Logger(__name__)

def create_tables():
    """Creates the database tables for the Book and User models."""
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    create_tables()
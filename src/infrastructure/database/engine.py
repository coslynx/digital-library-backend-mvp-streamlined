from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings

# Create a new SQLAlchemy engine based on the DATABASE_URL from settings.py.
engine = create_engine(settings.DATABASE_URL)

# Create a sessionmaker to create database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    """
    Provides a database session to the application.

    This function creates a new database session each time it is called,
    ensuring that each request has a fresh session. This helps to prevent
    data corruption and ensures that changes made by one request do not
    affect other requests.

    Args:
        None

    Returns:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
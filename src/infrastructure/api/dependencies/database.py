from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.settings import settings
from src.infrastructure.database.engine import engine
from src.infrastructure.database.models.base import Base

# Import SQLAlchemy's sessionmaker to create database sessions.
from sqlalchemy.orm import sessionmaker

# Import pydantic's BaseModel for defining Pydantic models.
from pydantic import BaseModel

# Create a new SQLAlchemy engine based on the DATABASE_URL from settings.py.
engine = create_engine(settings.DATABASE_URL)

# Create a sessionmaker to create database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a Pydantic model for the response of the get_db function.
class DatabaseResponse(BaseModel):
    message: str = "Database connection successful"

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
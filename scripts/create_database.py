from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models.base import Base
from src.config.settings import settings
from src.utils.logger import Logger

logger = Logger(__name__)

def create_database():
    """
    Creates the PostgreSQL database for the application.

    This function connects to the PostgreSQL server and creates the database
    specified in the DATABASE_URL environment variable.

    Args:
        None

    Returns:
        None

    Raises:
        DatabaseError: If an error occurs while creating the database.
    """
    # Extract database name from DATABASE_URL
    database_url = settings.DATABASE_URL
    database_name = database_url.split('/')[-1]

    # Connect to the PostgreSQL server
    engine = create_engine(database_url.replace(f'/{database_name}', ''))

    # Create the database
    try:
        with engine.connect() as connection:
            connection.execute(f"CREATE DATABASE {database_name}")
            logger.info(f"Database '{database_name}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise

if __name__ == "__main__":
    create_database()
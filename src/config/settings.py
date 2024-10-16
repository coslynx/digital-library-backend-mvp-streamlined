from pydantic import BaseSettings, Field
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".") / ".env")

class Settings(BaseSettings):
    """
    Configuration settings for the Streamlined Digital Library Backend.
    """
    
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    """
    Database connection URL. Read from the DATABASE_URL environment variable. 
    """

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    """
    Secret key for JWT token generation.  Read from the SECRET_KEY environment variable. 
    """

    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    """
    Logging level for the application.  Defaults to 'INFO'.  Read from the LOG_LEVEL environment variable. 
    """

    FRONTEND_URL: Optional[str] = Field(None, env="FRONTEND_URL")
    """
    URL of the frontend application. Used for CORS configuration.  Read from the FRONTEND_URL environment variable. 
    """

    LOG_FILE: Optional[str] = Field(None, env="LOG_FILE")
    """
    Path to the log file. If not set, logs to console.  Read from the LOG_FILE environment variable. 
    """

    LOG_FILE_MAX_SIZE: int = Field(10000000, env="LOG_FILE_MAX_SIZE")
    """
    Maximum size of the log file in bytes before rotating.  Defaults to 10MB.  Read from the LOG_FILE_MAX_SIZE environment variable. 
    """

    LOG_FILE_BACKUP_COUNT: int = Field(5, env="LOG_FILE_BACKUP_COUNT")
    """
    Number of backup log files to keep. Defaults to 5.  Read from the LOG_FILE_BACKUP_COUNT environment variable. 
    """

    GOOGLE_BOOKS_API_KEY: Optional[str] = Field(None, env="GOOGLE_BOOKS_API_KEY")
    """
    API key for the Google Books API.  Read from the GOOGLE_BOOKS_API_KEY environment variable. 
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
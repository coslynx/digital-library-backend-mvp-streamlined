import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional

from src.config.settings import settings


class Logger:
    """
    A custom logger class for the application.

    This class provides a centralized and configurable logging system that
    supports various log levels, output destinations, and message formatting.
    """

    def __init__(self, name: str):
        """
        Initializes the logger instance.

        Args:
            name: The name of the logger.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

        # Create a formatter for log messages.
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create a handler for logging to the console.
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create a handler for logging to a file.
        if settings.LOG_FILE:
            file_handler = RotatingFileHandler(
                settings.LOG_FILE,
                maxBytes=settings.LOG_FILE_MAX_SIZE,
                backupCount=settings.LOG_FILE_BACKUP_COUNT,
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str, *args: Any):
        """
        Logs a debug message.

        Args:
            message: The debug message.
            *args: Optional arguments for message interpolation.
        """
        self.logger.debug(message, *args)

    def info(self, message: str, *args: Any):
        """
        Logs an info message.

        Args:
            message: The info message.
            *args: Optional arguments for message interpolation.
        """
        self.logger.info(message, *args)

    def warning(self, message: str, *args: Any):
        """
        Logs a warning message.

        Args:
            message: The warning message.
            *args: Optional arguments for message interpolation.
        """
        self.logger.warning(message, *args)

    def error(self, message: str, *args: Any):
        """
        Logs an error message.

        Args:
            message: The error message.
            *args: Optional arguments for message interpolation.
        """
        self.logger.error(message, *args)

    def critical(self, message: str, *args: Any):
        """
        Logs a critical message.

        Args:
            message: The critical message.
            *args: Optional arguments for message interpolation.
        """
        self.logger.critical(message, *args)
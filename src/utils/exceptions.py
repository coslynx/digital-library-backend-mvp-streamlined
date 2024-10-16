from typing import Any

class BaseException(Exception):
    """Base class for all custom exceptions in the application."""
    def __init__(self, message: str, status_code: int = 400, **kwargs: Any):
        super().__init__(message)
        self.status_code = status_code
        self.kwargs = kwargs

class AuthenticationError(BaseException):
    """Raised when an authentication error occurs."""
    def __init__(self, message: str, status_code: int = 401, **kwargs: Any):
        super().__init__(message, status_code, **kwargs)

class UserNotFoundError(BaseException):
    """Raised when a user is not found."""
    def __init__(self, message: str, status_code: int = 404, **kwargs: Any):
        super().__init__(message, status_code, **kwargs)

class InvalidCredentialsError(BaseException):
    """Raised when invalid credentials are provided."""
    def __init__(self, message: str, status_code: int = 401, **kwargs: Any):
        super().__init__(message, status_code, **kwargs)

class BookNotFoundError(BaseException):
    """Raised when a book is not found."""
    def __init__(self, message: str, status_code: int = 404, **kwargs: Any):
        super().__init__(message, status_code, **kwargs)

class InvalidISBNError(BaseException):
    """Raised when an invalid ISBN format is provided."""
    def __init__(self, message: str, status_code: int = 400, **kwargs: Any):
        super().__init__(message, status_code, **kwargs)

class DatabaseError(BaseException):
    """Raised when a database error occurs."""
    def __init__(self, message: str, status_code: int = 500, **kwargs: Any):
        super().__init__(message, status_code, **kwargs)
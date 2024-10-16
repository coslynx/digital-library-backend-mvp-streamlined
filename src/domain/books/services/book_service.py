from typing import Optional, List

from sqlalchemy.orm import Session

from src.domain.books.models.book import Book
from src.domain.books.repositories.book_repository import BookRepository
from src.utils.exceptions import BookNotFoundError, InvalidISBNError

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def create_book(self, session: Session, book: Book) -> Book:
        """
        Creates a new book in the database.

        Args:
            session: SQLAlchemy session.
            book: Book object representing the book to be created.

        Returns:
            Book: The newly created book object.

        Raises:
            InvalidISBNError: If the provided ISBN is invalid.
        """
        if not self._validate_isbn(book.isbn):
            raise InvalidISBNError("Invalid ISBN format")

        return self.book_repository.create(session, book)

    def get_book_by_id(self, session: Session, book_id: int) -> Book:
        """
        Retrieves a book by its ID.

        Args:
            session: SQLAlchemy session.
            book_id: The ID of the book to retrieve.

        Returns:
            Book: The retrieved book object.

        Raises:
            BookNotFoundError: If no book is found with the given ID.
        """
        book = self.book_repository.get_by_id(session, book_id)
        if not book:
            raise BookNotFoundError(f"Book with ID {book_id} not found.")
        return book

    def get_all_books(self, session: Session) -> List[Book]:
        """
        Retrieves all books from the database.

        Args:
            session: SQLAlchemy session.

        Returns:
            List[Book]: A list of all book objects.
        """
        return self.book_repository.get_all(session)

    def update_book(self, session: Session, book_id: int, book: Book) -> Book:
        """
        Updates an existing book in the database.

        Args:
            session: SQLAlchemy session.
            book_id: The ID of the book to update.
            book: Book object containing the updated book data.

        Returns:
            Book: The updated book object.

        Raises:
            BookNotFoundError: If no book is found with the given ID.
            InvalidISBNError: If the provided ISBN is invalid.
        """
        if not self._validate_isbn(book.isbn):
            raise InvalidISBNError("Invalid ISBN format")

        updated_book = self.book_repository.update(session, book_id, book)
        if not updated_book:
            raise BookNotFoundError(f"Book with ID {book_id} not found.")
        return updated_book

    def delete_book(self, session: Session, book_id: int) -> bool:
        """
        Deletes a book from the database.

        Args:
            session: SQLAlchemy session.
            book_id: The ID of the book to delete.

        Returns:
            bool: True if the book was deleted successfully, False otherwise.

        Raises:
            BookNotFoundError: If no book is found with the given ID.
        """
        deleted = self.book_repository.delete(session, book_id)
        if not deleted:
            raise BookNotFoundError(f"Book with ID {book_id} not found.")
        return deleted

    def find_book_by_isbn(self, session: Session, isbn: str) -> Optional[Book]:
        """
        Retrieves a book by its ISBN.

        Args:
            session: SQLAlchemy session.
            isbn: The ISBN of the book to retrieve.

        Returns:
            Optional[Book]: The retrieved book object, or None if not found.

        Raises:
            InvalidISBNError: If the provided ISBN is invalid.
        """
        if not self._validate_isbn(isbn):
            raise InvalidISBNError("Invalid ISBN format")

        return self.book_repository.find_by_isbn(session, isbn)

    def _validate_isbn(self, isbn: str) -> bool:
        """
        Validates the ISBN format using a simple check for length and character types.

        Args:
            isbn: The ISBN to validate.

        Returns:
            bool: True if the ISBN is valid, False otherwise.
        """
        # Implement more robust ISBN validation logic if needed.
        return len(isbn) == 13 and isbn.isdigit()
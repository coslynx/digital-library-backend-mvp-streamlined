from sqlalchemy.orm import Session

from src.domain.books.models.book import Book


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, book: Book) -> Book:
        """
        Creates a new book in the database.

        Args:
            book: Book object representing the book to be created.

        Returns:
            Book: The newly created book object.
        """
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Book:
        """
        Retrieves a book by its ID.

        Args:
            book_id: The ID of the book to retrieve.

        Returns:
            Book: The retrieved book object, or None if not found.
        """
        return self.session.query(Book).filter(Book.id == book_id).first()

    def get_all(self) -> list[Book]:
        """
        Retrieves all books from the database.

        Returns:
            list[Book]: A list of all book objects.
        """
        return self.session.query(Book).all()

    def update(self, book_id: int, book: Book) -> Book:
        """
        Updates an existing book in the database.

        Args:
            book_id: The ID of the book to update.
            book: Book object containing the updated book data.

        Returns:
            Book: The updated book object.
        """
        db_book = self.session.query(Book).filter(Book.id == book_id).first()
        if db_book:
            db_book.title = book.title
            db_book.author = book.author
            db_book.isbn = book.isbn
            db_book.description = book.description
            db_book.publication_date = book.publication_date
            db_book.language = book.language
            db_book.genre = book.genre
            db_book.cover_image = book.cover_image
            self.session.commit()
            self.session.refresh(db_book)
            return db_book
        else:
            return None

    def delete(self, book_id: int) -> bool:
        """
        Deletes a book from the database.

        Args:
            book_id: The ID of the book to delete.

        Returns:
            bool: True if the book was deleted successfully, False otherwise.
        """
        book = self.session.query(Book).filter(Book.id == book_id).first()
        if book:
            self.session.delete(book)
            self.session.commit()
            return True
        else:
            return False

    def find_by_isbn(self, isbn: str) -> Book:
        """
        Retrieves a book by its ISBN.

        Args:
            isbn: The ISBN of the book to retrieve.

        Returns:
            Book: The retrieved book object, or None if not found.
        """
        return self.session.query(Book).filter(Book.isbn == isbn).first()
import pytest
from unittest.mock import patch

from src.domain.books.services.book_service import BookService
from src.domain.books.models.book import Book
from src.utils.exceptions import BookNotFoundError, InvalidISBNError
from src.infrastructure.database.models.base import Base
from sqlalchemy.orm import Session

# Mock SQLAlchemy session
class MockSession:
    def __init__(self):
        self.added_objects = []

    def add(self, obj: Base):
        self.added_objects.append(obj)

    def commit(self):
        pass

    def refresh(self, obj: Base):
        pass

    def query(self, model):
        return self

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return None

@pytest.fixture
def mock_session():
    return MockSession()

@pytest.fixture
def book_service(mock_session):
    book_repository = BookRepository(session=mock_session)
    return BookService(book_repository=book_repository)

def test_create_book_success(book_service, mock_session):
    book = Book(title="Test Book", author="Test Author", isbn="97801234567890", description="This is a test book.")
    created_book = book_service.create_book(session=mock_session, book=book)
    assert created_book.title == "Test Book"
    assert created_book.author == "Test Author"
    assert created_book.isbn == "97801234567890"
    assert created_book.description == "This is a test book."
    assert mock_session.added_objects[0] == book

def test_create_book_invalid_isbn(book_service, mock_session):
    book = Book(title="Test Book", author="Test Author", isbn="1234567890", description="This is a test book.")
    with pytest.raises(InvalidISBNError) as exc:
        book_service.create_book(session=mock_session, book=book)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid ISBN format"

def test_get_book_by_id_success(book_service, mock_session):
    book = Book(id=1, title="Test Book", author="Test Author", isbn="97801234567890", description="This is a test book.")
    mock_session.query(Book).filter(Book.id == 1).first = lambda: book
    retrieved_book = book_service.get_book_by_id(session=mock_session, book_id=1)
    assert retrieved_book.id == 1
    assert retrieved_book.title == "Test Book"

def test_get_book_by_id_not_found(book_service, mock_session):
    with pytest.raises(BookNotFoundError) as exc:
        book_service.get_book_by_id(session=mock_session, book_id=999)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Book with ID 999 not found."

def test_get_all_books(book_service, mock_session):
    book1 = Book(id=1, title="Test Book 1", author="Test Author 1", isbn="97801234567891", description="This is a test book 1.")
    book2 = Book(id=2, title="Test Book 2", author="Test Author 2", isbn="97801234567892", description="This is a test book 2.")
    mock_session.query(Book).all = lambda: [book1, book2]
    all_books = book_service.get_all_books(session=mock_session)
    assert len(all_books) == 2
    assert all_books[0].id == 1
    assert all_books[1].id == 2

def test_update_book_success(book_service, mock_session):
    book = Book(id=1, title="Test Book", author="Test Author", isbn="97801234567890", description="This is a test book.")
    mock_session.query(Book).filter(Book.id == 1).first = lambda: book
    updated_book = Book(title="Updated Test Book", author="Updated Test Author", isbn="97801234567890", description="This is an updated test book.")
    updated_book = book_service.update_book(session=mock_session, book_id=1, book=updated_book)
    assert updated_book.title == "Updated Test Book"
    assert updated_book.author == "Updated Test Author"
    assert updated_book.description == "This is an updated test book."

def test_update_book_not_found(book_service, mock_session):
    with pytest.raises(BookNotFoundError) as exc:
        book_service.update_book(session=mock_session, book_id=999, book=Book())
    assert exc.value.status_code == 404
    assert exc.value.detail == "Book with ID 999 not found."

def test_update_book_invalid_isbn(book_service, mock_session):
    book = Book(id=1, title="Test Book", author="Test Author", isbn="97801234567890", description="This is a test book.")
    mock_session.query(Book).filter(Book.id == 1).first = lambda: book
    updated_book = Book(title="Updated Test Book", author="Updated Test Author", isbn="1234567890", description="This is an updated test book.")
    with pytest.raises(InvalidISBNError) as exc:
        book_service.update_book(session=mock_session, book_id=1, book=updated_book)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid ISBN format"

def test_delete_book_success(book_service, mock_session):
    book = Book(id=1, title="Test Book", author="Test Author", isbn="97801234567890", description="This is a test book.")
    mock_session.query(Book).filter(Book.id == 1).first = lambda: book
    deleted = book_service.delete_book(session=mock_session, book_id=1)
    assert deleted is True

def test_delete_book_not_found(book_service, mock_session):
    with pytest.raises(BookNotFoundError) as exc:
        book_service.delete_book(session=mock_session, book_id=999)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Book with ID 999 not found."

def test_find_book_by_isbn_success(book_service, mock_session):
    book = Book(id=1, title="Test Book", author="Test Author", isbn="97801234567890", description="This is a test book.")
    mock_session.query(Book).filter(Book.isbn == "97801234567890").first = lambda: book
    found_book = book_service.find_book_by_isbn(session=mock_session, isbn="97801234567890")
    assert found_book.id == 1
    assert found_book.title == "Test Book"

def test_find_book_by_isbn_not_found(book_service, mock_session):
    mock_session.query(Book).filter(Book.isbn == "97801234567891").first = lambda: None
    found_book = book_service.find_book_by_isbn(session=mock_session, isbn="97801234567891")
    assert found_book is None

def test_find_book_by_isbn_invalid_isbn(book_service, mock_session):
    with pytest.raises(InvalidISBNError) as exc:
        book_service.find_book_by_isbn(session=mock_session, isbn="1234567890")
    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid ISBN format"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime

from src.config.settings import settings
from src.domain.books.models.book import Book
from src.infrastructure.api.dependencies.database import get_db
from src.infrastructure.api.v1.controllers.books_controller import BooksController
from src.domain.books.services.book_service import BookService
from src.domain.books.repositories.book_repository import BookRepository

from src.infrastructure.api.main import app

client = TestClient(app)
engine = create_engine(settings.DATABASE_URL)

@pytest.fixture(scope="module")
def db() -> Session:
    session = Session(engine)
    yield session
    session.close()

@pytest.fixture(scope="module")
def books_controller(db: Session) -> BooksController:
    book_service = BookService(book_repository=BookRepository(session=db))
    yield BooksController(book_service=book_service)

@pytest.fixture(scope="module")
def book_data():
    yield {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "97801234567890",
        "description": "This is a test book.",
        "publication_date": "2023-03-15",
        "language": "English",
        "genre": "Fiction",
        "cover_image": "https://example.com/cover.jpg",
    }

def test_create_book(books_controller: BooksController, db: Session, book_data):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 201
    book = db.query(Book).filter_by(isbn=book_data["isbn"]).first()
    assert book is not None
    assert book.title == book_data["title"]
    assert book.author == book_data["author"]
    assert book.isbn == book_data["isbn"]
    assert book.description == book_data["description"]
    assert book.publication_date == datetime.strptime(book_data["publication_date"], "%Y-%m-%d").date()
    assert book.language == book_data["language"]
    assert book.genre == book_data["genre"]
    assert book.cover_image == book_data["cover_image"]

def test_get_all_books(books_controller: BooksController, db: Session, book_data):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 201
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_book_by_id(books_controller: BooksController, db: Session, book_data):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 201
    book_id = response.json()["id"]
    response = client.get(f"/api/v1/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id

def test_update_book(books_controller: BooksController, db: Session, book_data):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 201
    book_id = response.json()["id"]
    updated_book_data = {
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "isbn": book_data["isbn"],
        "description": "This is an updated test book.",
        "publication_date": "2023-04-15",
        "language": "English",
        "genre": "Sci-Fi",
        "cover_image": "https://example.com/updated_cover.jpg",
    }
    response = client.put(f"/api/v1/books/{book_id}", json=updated_book_data)
    assert response.status_code == 200
    book = db.query(Book).filter_by(isbn=book_data["isbn"]).first()
    assert book.title == updated_book_data["title"]
    assert book.author == updated_book_data["author"]
    assert book.description == updated_book_data["description"]
    assert book.publication_date == datetime.strptime(updated_book_data["publication_date"], "%Y-%m-%d").date()
    assert book.genre == updated_book_data["genre"]
    assert book.cover_image == updated_book_data["cover_image"]

def test_delete_book(books_controller: BooksController, db: Session, book_data):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 201
    book_id = response.json()["id"]
    response = client.delete(f"/api/v1/books/{book_id}")
    assert response.status_code == 200
    book = db.query(Book).filter_by(isbn=book_data["isbn"]).first()
    assert book is None
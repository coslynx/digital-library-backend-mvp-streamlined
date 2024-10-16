from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from src.domain.books.models.book import Book
from src.domain.books.services.book_service import BookService
from src.infrastructure.api.dependencies.database import get_db

from src.infrastructure.api.v1.schemas.books import BookCreate, BookUpdate

class BooksController:
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    async def create_book(self, book: BookCreate, db: Session = Depends(get_db)):
        """Creates a new book in the database."""
        try:
            new_book = self.book_service.create_book(db, book)
            return new_book
        except HTTPException as e:
            raise e

    async def get_all_books(self, db: Session = Depends(get_db)):
        """Retrieves all books from the database."""
        try:
            all_books = self.book_service.get_all_books(db)
            return all_books
        except HTTPException as e:
            raise e

    async def get_book_by_id(self, book_id: int, db: Session = Depends(get_db)):
        """Retrieves a book by its ID."""
        try:
            book = self.book_service.get_book_by_id(db, book_id)
            return book
        except HTTPException as e:
            raise e

    async def update_book(self, book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
        """Updates an existing book in the database."""
        try:
            updated_book = self.book_service.update_book(db, book_id, book)
            return updated_book
        except HTTPException as e:
            raise e

    async def delete_book(self, book_id: int, db: Session = Depends(get_db)):
        """Deletes a book from the database."""
        try:
            deleted = self.book_service.delete_book(db, book_id)
            return deleted
        except HTTPException as e:
            raise e

def get_books_controller(book_service: BookService = Depends()):
    """Provides the BooksController instance as a FastAPI dependency."""
    return BooksController(book_service)
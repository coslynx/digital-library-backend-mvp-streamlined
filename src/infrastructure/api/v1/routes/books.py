from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.domain.books.models.book import Book
from src.domain.books.services.book_service import BookService
from src.infrastructure.api.dependencies.database import get_db

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)

@router.post("/", response_model=Book)
async def create_book(book: Book, db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Creates a new book entry in the database.

    Args:
        book: Book object containing the new book data.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        Book: The newly created book object.

    Raises:
        HTTPException: If an error occurs during book creation.
    """
    try:
        new_book = book_service.create_book(db, book)
        return new_book
    except HTTPException as e:
        raise e

@router.get("/", response_model=List[Book])
async def get_all_books(db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Retrieves all books from the database.

    Args:
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        List[Book]: A list of all book objects.

    Raises:
        HTTPException: If an error occurs during book retrieval.
    """
    try:
        all_books = book_service.get_all_books(db)
        return all_books
    except HTTPException as e:
        raise e

@router.get("/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Retrieves a book by its ID.

    Args:
        book_id: The ID of the book to retrieve.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        Book: The retrieved book object.

    Raises:
        HTTPException: If no book is found with the given ID or if an error occurs during retrieval.
    """
    try:
        book = book_service.get_book_by_id(db, book_id)
        return book
    except HTTPException as e:
        raise e

@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book, db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Updates an existing book in the database.

    Args:
        book_id: The ID of the book to update.
        book: Book object containing the updated book data.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        Book: The updated book object.

    Raises:
        HTTPException: If no book is found with the given ID or if an error occurs during update.
    """
    try:
        updated_book = book_service.update_book(db, book_id, book)
        return updated_book
    except HTTPException as e:
        raise e

@router.delete("/{book_id}", response_model=bool)
async def delete_book(book_id: int, db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Deletes a book from the database.

    Args:
        book_id: The ID of the book to delete.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        bool: True if the book was deleted successfully, False otherwise.

    Raises:
        HTTPException: If no book is found with the given ID or if an error occurs during deletion.
    """
    try:
        deleted = book_service.delete_book(db, book_id)
        return deleted
    except HTTPException as e:
        raise e
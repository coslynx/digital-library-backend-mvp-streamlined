from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.models.base import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=False, unique=True)
    description = Column(Text)
    publication_date = Column(DateTime)
    language = Column(String)
    genre = Column(String)
    cover_image = Column(String)

    borrow_history = relationship("Borrow", backref="book")

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')>"
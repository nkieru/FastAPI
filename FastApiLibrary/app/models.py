from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, text
from datetime import date
from typing import List
from app.database import Base, str_nullable, int_pk
from app.config import Genre


class Author(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    biography: Mapped[str_nullable]
    date_of_birth: Mapped[date]
    books: Mapped[List['Book']] = relationship('Book', secondary="authorbooks", back_populates="authors", lazy='selectin')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "biography": self.biography,
            "date_of_birth": self.date_of_birth,
            "books": self.books
        }


class Book(Base):
    id: Mapped[int_pk]
    title: Mapped[str]
    description: Mapped[str_nullable]
    publication_date: Mapped[date]
    authors: Mapped[List['Author']] = relationship("Author", secondary="authorbooks", back_populates='books', lazy='selectin')
    genre: Mapped[Genre]
    available_copies: Mapped[int]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "publication_date": self.publication_date,
            "authors": self.authors,
            "genre": self.genre,
            "available_copies": self.available_copies
        }


class AuthorBook(Base):
    id: Mapped[int_pk]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint('author_id', 'book_id', name='uq_author_book'),)

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "book_id": self.book_id
        }


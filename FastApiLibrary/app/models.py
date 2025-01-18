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


class Book(Base):
    id: Mapped[int_pk]
    title: Mapped[str]
    description: Mapped[str_nullable]
    publication_date: Mapped[date]
    authors: Mapped[List['Author']] = relationship("Author", secondary="authorbooks", back_populates='books', lazy='selectin')
    genre: Mapped[Genre]
    available_copies: Mapped[int]


class AuthorBook(Base):
    id: Mapped[int_pk]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint('author_id', 'book_id', name='uq_author_book'),)

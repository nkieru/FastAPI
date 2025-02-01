from sqlalchemy import select
from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import date
from typing import Optional
from app.database import async_session_maker
from app.models import Book, Author
from app.config import Genre



class AuthorFilter(Filter):
    name__in: Optional[list[str]] | None = None
    date_of_birth__gte: Optional[date] | None = None

    class Constants(Filter.Constants):
        model = Author

    def to_dict(self) -> dict:
        return {key: value for key, value in
                {
            'id': self.id,
            'name': self.name,
            'biography': self.biography,
            'date_of_birth': self.date_of_birth,
            'books': self.books,
                }.items() if value is not None
                }


async def author_filter_data(author_filter: AuthorFilter):
    async with async_session_maker() as session:
        query = author_filter.filter(select(Author))
        return await paginate(session, query)



class BookFilter(Filter):
    title__in: Optional[list[str]] | None = None
    publication_date__gte: Optional[date] | None = None
    genre: Optional[Genre] | None = None
    available_copies__gte: Optional[int] | None = None

    class Constants(Filter.Constants):
        model = Book


async def book_filter_data(book_filter: BookFilter):
    async with async_session_maker() as session:
        query = book_filter.filter(select(Book))
        return await paginate(session, query)

from sqlalchemy import select, update, delete
from app.filters import *
from app.schemas import BookUpdateSchema, AuthorUpdateSchema
from app.models import Author, Book

from fastapi_pagination.ext.sqlalchemy import paginate


async def find_id_data(model, model_id):
    async with async_session_maker() as session:
        query = select(model).filter_by(id=model_id)
        result = await session.execute(query)
        model_info = result.scalar_one_or_none()
        if not model_info:
            return None
        else:
            model_data = model_info.to_dict()
            return model_data


async def find_all_data(model):
    async with async_session_maker() as session:
        query = select(model)
        result = await session.execute(query)
        model_info = result.scalars().all()
        if not model_info:
            return None
        else:
            return await paginate(session, query)


async def find_email(model, model_email):
    async with async_session_maker() as session:
        query = select(model).filter_by(email=model_email)
        result = await session.execute(query)
        model_info = result.scalar_one_or_none()
        if not model_info:
            return None
        else:
            model_data = model_info.to_dict()
            return model_data


async def add_object(model, **data):
    async with async_session_maker() as session:
        async with session.begin():
            new_model = model(**data)
            session.add(new_model)
            await session.flush()
            new_model_id = new_model.id
            await session.commit()
            return new_model_id


async def delete_object(model, model_id: int):
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(delete(model).filter_by(id=model_id))
            await session.commit()
            return model_id


async def change_book(book_id: int, book: BookUpdateSchema, find_book) -> dict:
    async with async_session_maker() as session:

        book_to_change_dict = Book(**find_book).to_dict()

        query = select(Book).filter_by(id=book_id)
        result = await session.execute(query)
        book_to_change = result.scalar_one_or_none()

        book = book.model_dump(exclude_unset=True)
        put_data = {key: book.get(key, book_to_change_dict[key]) for key in book if book[key]}
        book_to_change.title = put_data['title'] if 'title' in put_data else book_to_change_dict['title']
        book_to_change.description = put_data['description'] if 'description' in put_data else book_to_change_dict['description']
        book_to_change.publication_date = put_data['publication_date'] if 'publication_date' in put_data else book_to_change_dict['publication_date']
        book_to_change.genre = put_data['genre'] if 'genre' in put_data else book_to_change_dict['genre']
        book_to_change.available_copies = put_data['available_copies']  if 'available_copies' in put_data else book_to_change_dict['available_copies']
        await session.commit()
        return put_data


async def change_author(author_id: int, author: AuthorUpdateSchema, find_author) -> dict:
    async with async_session_maker() as session:

        author_to_change_dict = Author(**find_author).to_dict()

        query = select(Author).filter_by(id=author_id)
        result = await session.execute(query)
        author_to_change = result.scalar_one_or_none()

        author = author.model_dump(exclude_unset=True)
        put_data = {key: author.get(key, author_to_change_dict[key]) for key in author if author[key]}
        author_to_change.name = put_data['name'] if 'name' in put_data else author_to_change_dict['name']
        author_to_change.biography = put_data['biography'] if 'biography' in put_data else author_to_change_dict['biography']
        author_to_change.date_of_birth = put_data['date_of_birth'] if 'date_of_birth' in put_data else author_to_change_dict['date_of_birth']
        await session.commit()
        return put_data

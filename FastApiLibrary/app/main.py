from fastapi import FastAPI
from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, add_pagination
from sqlalchemy import select, update, delete
from app.filters import *
from app.schemas import BookSchema, AuthorSchema, BookSchemaAdd, AuthorSchemaAdd, AuthorBookSchema, BookUpdateSchema
from app.models import AuthorBook



app = FastAPI()

router_books = APIRouter(prefix='/books', tags=['Список книг'])
router_authors = APIRouter(prefix='/authors', tags=['Список авторов'])


@app.get("/")
def home_page():
    return {"message": "Hello!"}


@router_books.get("/{book_id}", summary="Get book by id")
async def get_book_by_id(book_id: int) -> BookSchema | dict:
    result = await find_id_data(model=Book, model_id=book_id)
    if result is None:
        return {'message': f'Book ID = {book_id} not found!'}
    else:
        return result


@router_authors.get("/{author_id}", summary="Get author by id")
async def get_author_by_id(author_id: int) -> AuthorSchema | dict:
    result = await find_id_data(model=Author, model_id=author_id)
    if result is None:
        return {'message': f'Author ID = {author_id} not found!'}
    else:
        return result


@router_books.get("/", summary="Get filter books")
async def get_filter_books(book_filter: BookFilter = FilterDepends(BookFilter)) -> Page[BookSchema]:
    result = await book_filter_data(book_filter)
    return result


@router_authors.get("/", summary="Get filter authors")
async def get_filter_authors(author_filter: AuthorFilter = FilterDepends(AuthorFilter)) -> Page[AuthorSchema]:
    result = await author_filter_data(author_filter)
    return result


@router_books.post("/add_book/")
async def create_book(book: BookSchemaAdd = Depends()) -> BookSchema | dict:
    result = await add_book(**book.to_dict())
    return {"message": f"Book created! ID={result} {book}."}


async def add_book(**book_data: BookSchemaAdd):
    async with async_session_maker() as session:
        async with session.begin():
            new_book = Book(**book_data)
            session.add(new_book)
            await session.flush()
            new_book_id = new_book.id
            await session.commit()
            return new_book_id


@router_authors.post("/add_author/")
async def create_book(author: AuthorSchemaAdd = Depends()) -> AuthorSchema | dict:
    result = await add_author(**author.to_dict())
    return {"message": f"Author created! ID={result} {author}."}


async def add_author(**author_data: AuthorSchemaAdd):
    async with async_session_maker() as session:
        async with session.begin():
            new_author = Author(**author_data)
            session.add(new_author)
            await session.flush()
            new_author_id = new_author.id
            await session.commit()
            return new_author_id


@router_authors.post('/relation_author_book/')
async def author_book_relation(relation: AuthorBookSchema = Depends()):
    result = await add_author_book(**relation.to_dict())
    return {"message": f"Relation created! ID={result} {relation}."}


async def add_author_book(**author_book_data: AuthorBookSchema):
    async with async_session_maker() as session:
        async with session.begin():
            new_relation = AuthorBook(**author_book_data)
            session.add(new_relation)
            await session.flush()
            new_relation_id = new_relation.id
            await session.commit()
            return new_relation_id


@router_books.delete("/{book_id}/delete", summary="Delete book")
async def delete_book_by_id(book_id: int):
    book_to_delete = await find_id_data(model=Book, model_id=book_id)
    if book_to_delete is None:
        return {'message': f'Book ID = {book_id} not found!'}
    else:
        await delete_book(book_id=book_id)
        return {"message": f"Book with ID {book_id} deleted!"}


async def delete_book(book_id: int):
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(delete(Book).filter_by(id=book_id))
            await session.commit()
            return book_id


@router_authors.delete("/{author_id}/delete", summary="Delete author")
async def delete_author_by_id(author_id: int):
    author_to_delete = await find_id_data(model=Author, model_id=author_id)
    if author_to_delete is None:
        return {'message': f'Book ID = {author_id} not found!'}
    else:
        await delete_author(author_id=author_id)
        return {"message": f"Book with ID {author_id} deleted!"}


async def delete_author(author_id: int):
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(delete(Author).filter_by(id=author_id))
            await session.commit()
            return author_id


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


# @router_books.patch("/{book_id}/patch", summary="Update book")
# async def patch_book_by_id(book_id: int, book: BookUpdateSchema = Depends()) -> BookSchema | dict:
#     find_book = await find_id_data(model=Book, model_id=book_id)
#     result = await patch_book(find_book, book)
#     return {"message": f"Book {find_book} updated to {result}."}
#
#
# async def patch_book(find_book, book: BookUpdateSchema):
#     async with async_session_maker() as session:
#         async with session.begin():
#             book_model = Book(**find_book).to_dict()
#             update_data = book.dict(exclude_unset=True)
#             put_data = {key: update_data.get(key, book_model[key]) for key in update_data if update_data[key]}
#             book_model |= put_data
#             # await session.add(book_model)
#             await session.commit()
#             return book_model


app.include_router(router_books)
app.include_router(router_authors)

add_pagination(app)

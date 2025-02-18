from fastapi import FastAPI
from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, add_pagination
from app.models import AuthorBook
from app.utils import *
from app.schemas import *
from app.users.router import router_users



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


@router_books.post("/add_book/", summary="Add book")
async def create_book(book: BookSchemaAdd = Depends()) -> BookSchema | dict:
    result = await add_object(Book, **book.to_dict())
    return {"message": f"Book created! ID={result} {book}."}


@router_authors.post("/add_author/", summary="Add author")
async def create_author(author: AuthorSchemaAdd = Depends()) -> AuthorSchema | dict:
    result = await add_object(Author, **author.to_dict())
    return {"message": f"Author created! ID={result} {author}."}


@router_authors.post('/relation_author_book/', summary="Add author_book relation")
async def create_author_book_relation(relation: AuthorBookSchema = Depends()):
    result = await add_object(AuthorBook, **relation.to_dict())
    return {"message": f"Relation created! ID={result} {relation}."}


@router_books.delete("/{book_id}/delete", summary="Delete book")
async def delete_book_by_id(book_id: int):
    book_to_delete = await find_id_data(model=Book, model_id=book_id)
    if book_to_delete is None:
        return {'message': f'Book ID = {book_id} not found!'}
    else:
        await delete_object(model=Book, model_id=book_id)
        return {"message": f"Book with ID {book_id} deleted!"}


@router_authors.delete("/{author_id}/delete", summary="Delete author")
async def delete_author_by_id(author_id: int):
    author_to_delete = await find_id_data(model=Author, model_id=author_id)
    if author_to_delete is None:
        return {'message': f'Book ID = {author_id} not found!'}
    else:
        await delete_object(model=Author, model_id=author_id)
        return {"message": f"Book with ID {author_id} deleted!"}


@router_books.patch("/{book_id}/patch", summary="Update book")
async def patch_book_by_id(book_id: int, book: BookUpdateSchema = Depends()) -> BookSchema | dict:
    find_book = await find_id_data(model=Book, model_id=book_id)
    result = await change_book(book_id, book, find_book)
    return {'message': f"Book: {find_book}. Changes: {result}."}


@router_authors.patch("/{author_id}/patch", summary="Update author")
async def patch_author_by_id(author_id: int, author: AuthorUpdateSchema = Depends()) -> AuthorSchema | dict:
    find_author = await find_id_data(model=Author, model_id=author_id)
    result = await change_author(author_id, author, find_author)
    return {'message': f"Author: {find_author}. Changes: {result}."}


app.include_router(router_books)
app.include_router(router_authors)
app.include_router(router_users)

add_pagination(app)

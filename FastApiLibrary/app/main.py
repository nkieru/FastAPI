from fastapi import FastAPI
from fastapi import APIRouter
from sqlalchemy import select
from typing import List
from app.schemas import BookSchema
from app.database import async_session_maker
from app.models import Book


app = FastAPI()
router = APIRouter(prefix='/books', tags=['Список книг'])


@app.get("/")
def home_page():
    return {"message": "Hello!"}


# @router.get("/", summary="Получить список книг")
# async def get_all_books():
#     async with async_session_maker(expire_on_commit=False) as session:
#         query = select(Book)
#         result = await session.execute(query)
#         books = result.scalars().all()
#         return books


@router.get("/", summary="Получить все книги")
async def get_all_books() -> List[BookSchema]:
    async with async_session_maker(expire_on_commit=False) as session:
        query = select(Book)
        result = await session.execute(query)
        books = result.scalars().all()
        return books


app.include_router(router)

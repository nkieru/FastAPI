from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import date, datetime
from typing import List
from app.config import Genre


class AuthorSchema(BaseModel):
    id: int
    name: str = Field(default=..., min_length=1, max_length=100, description="Имя автора, от 1 до 100 символов")
    biography: str = Field(default='Нет описания', min_length=0, max_length=500, description="Биография автора, от 1 до 500 символов")
    date_of_birth: date = Field(default=..., description="Дата рождения автора в формате ГГГГ-ММ-ДД")
    # books: List['BookSchema'] = []

    @field_validator("date_of_birth")
    @classmethod
    def validate_publication_date(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения автора должна быть в прошлом ')
        return values


class BookSchema(BaseModel):
    id: int
    title: str = Field(default=..., min_length=1, max_length=100, description="Название книги, от 1 до 100 символов")
    description: str = Field(default='Нет описания', min_length=0, max_length=500, description="Описание книги, от 1 до 500 символов")
    publication_date: date = Field(default=..., description="Дата публикации книги в формате ГГГГ-ММ-ДД")
    genre: Genre = Field(default=..., description="Жанры книги")
    available_copies: int = Field(default=..., ge=0, description="Количество экземпляров не может быть меньше нуля")
    authors: List['AuthorSchema'] = []

    @field_validator("publication_date")
    @classmethod
    def validate_publication_date(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата публикации должна быть до текущей даты ')
        return values

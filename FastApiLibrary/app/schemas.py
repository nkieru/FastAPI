from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, text
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import date, datetime
from typing import List, Optional
from app.config import Genre


class AuthorSchema(BaseModel):
    id: int
    name: str = Field(default=..., min_length=1, max_length=100, description="Имя автора, от 1 до 100 символов")
    biography: Optional[str] = Field(None, max_length=500, description="Биография автора, до 500 символов")
    date_of_birth: date = Field(default=..., description="Дата рождения автора в формате ГГГГ-ММ-ДД")
    books: List['BookTitleSchema'] = []
    class Config:
        orm_mode = True

    @field_validator("date_of_birth")
    @classmethod
    def validate_publication_date(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения автора должна быть в прошлом ')
        return values


class BookSchema(BaseModel):
    id: int
    title: str = Field(default=..., min_length=1, max_length=100, description="Название книги, от 1 до 100 символов")
    description: Optional[str] = Field(None, max_length=500, description="Описание книги, до 500 символов")
    publication_date: date = Field(default=..., description="Дата публикации книги в формате ГГГГ-ММ-ДД")
    genre: Genre = Field(default=..., description="Жанры книги")
    available_copies: int = Field(default=..., ge=0, description="Количество экземпляров не может быть меньше нуля")
    authors: List['AuthorNameSchema'] = []

    class Config:
        orm_mode = True

    @field_validator("publication_date")
    @classmethod
    def validate_publication_date(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата публикации должна быть до текущей даты ')
        return values


class BookSchemaAdd(BaseModel):
    title: str = Field(default=..., min_length=1, max_length=100, description="Название книги, от 1 до 100 символов")
    description: Optional[str] = Field(None, max_length=500, description="Описание книги, до 500 символов")
    publication_date: date = Field(default=..., description="Дата публикации книги в формате ГГГГ-ММ-ДД")
    genre: Genre = Field(default=..., description="Жанры книги")
    available_copies: int = Field(default=..., ge=0, description="Количество экземпляров не может быть меньше нуля")

    class Config:
        orm_mode = True

    @field_validator("publication_date")
    @classmethod
    def validate_publication_date(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата публикации должна быть до текущей даты ')
        return values

    def to_dict(self) -> dict:
        return {key: value for key, value in
                {
            'title': self.title,
            'description': self.description,
            'publication_date': self.publication_date,
            'genre': self.genre,
            'available_copies': self.available_copies
                }.items() if value is not None
                }


class AuthorSchemaAdd(BaseModel):
    name: str = Field(default=..., min_length=1, max_length=100, description="Имя автора, от 1 до 100 символов")
    biography: Optional[str] = Field(None, max_length=500, description="Биография автора, до 500 символов")
    date_of_birth: date = Field(default=..., description="Дата рождения автора в формате ГГГГ-ММ-ДД")

    class Config:
        orm_mode = True

    @field_validator("date_of_birth")
    @classmethod
    def validate_publication_date(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения автора должна быть в прошлом ')
        return values

    def to_dict(self):
        return {
            "name": self.name,
            "biography": self.biography,
            "date_of_birth": self.date_of_birth
        }


class AuthorBookSchema(BaseModel):
    author_id: int = Field(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    book_id: int = Field(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    class Config:
        orm_mode = True

    def to_dict(self):
        return {
            "author_id": self.author_id,
            "book_id": self.book_id
        }

class BookUpdateSchema(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Название книги, от 1 до 100 символов")
    description: Optional[str] = Field(None, max_length=500, description="Описание книги, до 500 символов")
    publication_date: Optional[date] = Field(default=None, description="Дата публикации книги в формате ГГГГ-ММ-ДД")
    genre: Optional[Genre] = Field(default=None, description="Жанры книги")
    available_copies: Optional[int] = Field(default=None, ge=0, description="Количество экземпляров не может быть меньше нуля")

    class Config:
        orm_mode = True



class BookTitleSchema(BaseModel):
    title: str = Field(default=..., min_length=1, max_length=100, description="Название книги, от 1 до 100 символов")


class AuthorNameSchema(BaseModel):
    name: str = Field(default=..., min_length=1, max_length=100, description="Имя автора, от 1 до 100 символов")

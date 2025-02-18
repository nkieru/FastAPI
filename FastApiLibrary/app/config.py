from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import join, dirname
from enum import Enum


class Settings(BaseSettings):
    DB_PASS: str
    DB_LOGIN: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=join(dirname(__file__), '.env'), extra="ignore")


settings = Settings()


def db_url():
    return (f"postgresql+asyncpg://{settings.DB_LOGIN}:{settings.DB_PASS}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


class Genre(str, Enum):
    genre_1 = "Genre_1"
    genre_2 = "Genre_2"
    genre_3 = "Genre_3"
    genre_4 = "Genre_4"
    genre_5 = "Genre_5"

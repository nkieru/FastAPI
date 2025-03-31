from pydantic import EmailStr
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

from app.config import get_auth_data
from app.utils import find_email
from app.users.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


async def authenticate_user(user_email: EmailStr, password: str):
    user = await find_email(model=User, model_email=user_email)
    if user is None or verify_password(plain_password=password, hashed_password=user['password']) is False:
        return None
    else:
        return user

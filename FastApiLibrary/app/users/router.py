from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_pagination import Page

from app.users.auth import get_password_hash
from app.users.schemas import UserSchema, UserListSchema
from app.utils import *
from app.users.models import User


router_users = APIRouter(prefix='/users', tags=['Список пользователей'])


@router_users.post("/register/",  summary="Add user")
async def create_user(user_data: UserSchema = Depends()) -> dict:
    result = await find_email(model=User, model_email=user_data.email)
    if result is None:
        user_dict = user_data.dict()
        user_dict['password'] = get_password_hash(user_data.password)
        await add_object(User, **user_dict)
        user_first_name = user_dict['first_name']
        user_last_name = user_dict['last_name']
        return {'message': f'Registration user: {user_first_name} {user_last_name} successfully complete'}
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )


@router_users.get("/", summary="Get all users")
async def get_all_users() -> Page[UserListSchema]:
    async with async_session_maker(expire_on_commit=False):
        result = await find_all_data(model=User)
        return result

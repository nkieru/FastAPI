from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi_pagination import Page

from app.users.auth import get_password_hash
from app.users.schemas import UserSchema, UserListSchema, UserAuthSchema
from app.utils import *
from app.users.models import User
from app.users.auth import *
from app.users.dependencies import get_current_user


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


@router_users.post("/login/", summary="Login user")
async def auth_user(response: Response, user_data: UserAuthSchema = Depends()):
    check = await authenticate_user(user_email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    else:
        access_token = create_access_token({"sub": str(check['id'])})
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)
        return {'access_token': access_token, 'refresh_token': None}


@router_users.get("/", summary="Get all users")
async def get_all_users() -> Page[UserListSchema]:
    async with async_session_maker(expire_on_commit=False):
        result = await find_all_data(model=User)
        return result


@router_users.get("/my_data/", summary="Get me")
async def get_my_data(user_data: User = Depends(get_current_user)):
    return user_data


@router_users.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Logged out successfully'}

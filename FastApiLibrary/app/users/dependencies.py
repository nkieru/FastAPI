from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.config import get_auth_data
from app.utils import find_id_data
from app.main import *
from app.users.models import User



def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        decode_token = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='The token is not valid')

    expire = decode_token.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='The token has expired')

    user_id = decode_token.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID not found')

    user = await find_id_data(model=User, model_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user

from typing import List

from fastapi import APIRouter, HTTPException, Depends

from server import auth
from rest.model.user import UserRegister, UserLogin, UserOut, Token
from backend.users import add_user, get_user, get_users


user = APIRouter(
    prefix = '/user',
    tags   = ['user'],
)


@user.post('/register',
    status_code = 201,
    description = 'User Register',
)
async def register(user: UserRegister):
    if user.username in (u.username for u in get_users()):
        raise HTTPException(
            status_code = 400,
            detail      = 'Username already exists',
        )
    try:
        add_user(
            name = user.username,
            role = user.role,
            pswd = user.password1,
        )
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Add User Error ! {x}',
        )


@user.post('/login',
    status_code = 200,
    description = 'User login',
    response_model = Token,
)
async def login(login: UserLogin):
    user = get_user(login.username)
    if user:
        verified = auth.verify(login.password, user.password)
        if verified:
            token = auth.encode(
                user = user.username,
                role = user.role,
            )
            return Token(access_token=token)

    raise HTTPException(
        status_code = 401,
        detail      = 'Invalid credentials',
    )


@user.get('/{name}',
    status_code    = 200,
    description    = 'Get a User',
    response_model = UserOut,
)
async def get_one(name, user: str = Depends(auth.admin)):
    return get_user(name)


@user.get('',
    status_code    = 200,
    description    = 'Get all Users',
    response_model = List[UserOut],
)
async def get_all(user: str = Depends(auth.admin)):
    return get_users()

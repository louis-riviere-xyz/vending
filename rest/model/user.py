from typing import Optional

from fastapi import HTTPException
from pydantic import validator
from sqlmodel import SQLModel, Field

from backend.model.user import Role


class UserRegister(SQLModel):
    username:  str
    password1: str = Field(min_length=9, max_length=99)
    password2: str
    role:      Role

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise HTTPException(
                status_code = 400,
                detail      = "passwords don't match",
            )
        return v


class UserLogin(SQLModel):
    username   : str
    password   : str


class UserOut(SQLModel):
    username: str
    role    : str


class Token(SQLModel):
    access_token: str
    token_type:  Optional[str] = 'Bearer'

from enum import Enum

from sqlmodel import SQLModel, Field


class Role(str, Enum):
    admin  = 'admin',
    seller = 'seller'
    buyer  = 'buyer'


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password: str
    role:     Role
    deposit:  int = 0

from fastapi import HTTPException
from pydantic import validator
from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    name:      str = Field(primary_key=True)
    seller:    str
    cost:      int
    available: int = 1

    @validator('cost')
    def cost_valid(cls, cost, values, **kwargs):
        if cost % 5:
            raise HTTPException(
                status_code = 400,
                detail      = f'Invalid cost {cost}',
            )
        return cost

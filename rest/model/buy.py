from typing import List

from sqlmodel import SQLModel


class BuyReq(SQLModel):
    product  : str
    quantity : int


class BuyResp(SQLModel):
    total  : int
    change : List[int]



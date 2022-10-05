from sqlmodel import SQLModel


class ProductCre(SQLModel):
    name   : str
    seller : str
    cost   : int


class ProductOut(SQLModel):
    name      : str
    seller    : str
    cost      : int
    available : int



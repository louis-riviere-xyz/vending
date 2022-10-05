from sqlmodel import select

from backend.database import get_session, insert, update, delete
from backend.users import get_sellers
from backend.model.product import Product


def get_product(name):
    with get_session() as session:
        req = select(Product).where(
            Product.name == name
        )
        product = session.exec(req).first()
    return product


def get_products():
    with get_session() as session:
        req = select(Product)
        products = session.exec(req).all()
    return {p.name:p for p in products}


def cre_product(*, name, seller, cost):
    if get_product(name):
        raise ValueError(f'{name} already exists')

    if seller in get_sellers():
        insert(Product(
            name = name,
            seller = seller,
            cost = cost,
        ))
    else:
        raise ValueError(f'Invalid Seller {seller}')


def add_product(name):
    product = get_product(name)
    if product:
        product.available += 1
        update(product)
    else:
        raise ValueError(f'Product {name} Not Found')


def del_product(name):
    product = get_product(name)
    if product:
        if product.available > 0:
            product.available -= 1
            update(product)
        else:
            delete(product)
    else:
        raise ValueError(f'Product {name} Not Found')

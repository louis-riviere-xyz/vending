from backend.database import init_db
from backend.users import add_user
from backend.products import cre_product, add_product


def init_users():
    add_user(
        name = 'admin',
        role = 'admin',
        pswd = '123456789',
    )
    add_user(
        name = 'sam',
        role = 'seller',
        pswd = '123456789',
    )
    add_user(
        name = 'bob',
        role = 'buyer',
        pswd = '123456789',
    )


def init_products():
    cre_product(
        name = 'apple',
        seller = 'sam',
        cost = 100,
    )
    cre_product(
        name = 'banana',
        seller = 'sam',
        cost = 50,
    )
    add_product(
        name = 'banana',
    )


def populate():
    init_db()
    init_users()
    init_products()


if __name__=='__main__':
    populate()

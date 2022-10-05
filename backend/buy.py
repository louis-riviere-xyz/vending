from backend.database import get_session, update
from backend.users import get_user
from backend.products import get_product


coins = (100, 50, 20, 10, 5)


def add_coin(*, name, coin):
    if coin in  coins:
        user = get_user(name)
        user.deposit += coin
        update(user)
    else:
        raise ValueError('Invalid Deposit Amount')
    return user.deposit


def reset(name):
    user = get_user(name)
    user.deposit = 0
    update(user)
    return user.deposit


def make_change(amount):
    change = []
    for coin in coins:
        while amount >= coin:
            change.append(coin)
            amount -= coin
    return change


def buy_products(req, user):
    product = get_product(req.product)
    if product:
        quantity = req.quantity
        if quantity > 0:
            if product.available >= quantity:
                total = product.cost * quantity
                buyer = get_user(user)
                if buyer and buyer.deposit >= total:
                    buyer.deposit -= total
                    product.available-= quantity
                    with get_session() as session:
                        session.add(product)
                        session.add(buyer)
                        session.commit()
                        session.refresh(buyer)
                else:
                    raise ValueError('Insufficient Deposit')
            else:
                raise ValueError('Insufficient Products')
        else:
            raise ValueError('Quantity must be > 0')
    else:
        raise ValueError(f'Unkwnow Product : {req.product}')

    change = make_change(buyer.deposit)

    return dict(
        total  = total,
        change = change,
    )



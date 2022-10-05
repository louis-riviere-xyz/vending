from backend.users import get_user
from backend.products import get_product


def test_buy(buyer, seller):
    buyer.patch('/reset')
    bob = get_user('bob')
    assert bob.deposit == 0
    for i in range(5):
        buyer.patch('/deposit/100')
    buyer.patch('/deposit/50')
    buyer.patch('/deposit/20')
    buyer.patch('/deposit/20')
    buyer.patch('/deposit/5')
    bob = get_user('bob')
    assert bob.deposit == 595

    apple = get_product('apple')
    assert apple.available == 1

    for i in range(5):
        seller.put('/product/apple')

    apple = get_product('apple')
    assert apple.available == 6
    assert apple.cost == 100

    response = buyer.post('/buy',
        json = dict(
            product = 'apple',
            quantity = 5
        ),
    )
    assert response.status_code == 200

    bob = get_user('bob')

    data = response.json()
    assert data['total'] == 500
    assert sum(data['change']) == bob.deposit
    assert data['change'] == [50, 20, 20, 5]


def test_buy_bad_product(buyer):
    response = buyer.post('/buy',
        json = dict(
            product = 'melon',
            quantity = 5
        ),
    )
    assert response.status_code == 400


def test_buy_bad_deposit(buyer, seller):
    for i in range(5):
        seller.put('/product/apple')

    response = buyer.post('/buy',
        json = dict(
            product = 'apple',
            quantity = 5
        ),
    )
    assert response.status_code == 400


def test_buy_bad_quantity(buyer):
    for i in range(5):
        buyer.patch('/deposit/100')

    response = buyer.post('/buy',
        json = dict(
            product = 'apple',
            quantity = 10
        ),
    )
    assert response.status_code == 400


def test_buy_bad_zero(buyer):
    response = buyer.post('/buy',
        json = dict(
            product = 'apple',
            quantity = 0
        ),
    )
    assert response.status_code == 400

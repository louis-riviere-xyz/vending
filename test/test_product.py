from backend.products import get_product


def test_get_product(buyer):
    response = buyer.get('/product/banana')
    assert response.status_code == 200


def test_get_products(seller):
    response = seller.get('/product')
    assert response.status_code == 200


def test_get_product_missing(buyer):
    response = buyer.get('/product/wrong')
    assert response.status_code == 404


def test_create_incomplete(seller):
    response = seller.post('/product',
        json = dict(
            name = 'cantaloupe',
            seller = 'sam',
        ),
    )
    assert response.status_code == 444


def test_create_invalid_seller(seller):
    response = seller.post('/product',
        json = dict(
            name = 'cantaloupe',
            seller = 'toto',
        ),
    )
    assert response.status_code == 444


def test_create_invalid_cost(seller):
    response = seller.post('/product',
        json = dict(
            name = 'cantaloupe',
            seller = 'sam',
            cost = 33,
        ),
    )
    assert response.status_code == 400


def test_create_unauthorized(buyer):
    response = buyer.post('/product',
        json = dict(
            name = 'cantaloupe',
            seller = 'sam',
            cost = 150,
        ),
    )
    assert response.status_code == 401


def test_create(seller):
    assert not get_product('cantaloupe')

    response = seller.post('/product',
        json = dict(
            name = 'cantaloupe',
            seller = 'sam',
            cost = 150,
        ),
    )
    assert response.status_code == 201

    cantaloupe = get_product('cantaloupe')
    assert cantaloupe.available == 1


def test_add_one(seller):
    cantaloupe = get_product('cantaloupe')
    assert cantaloupe.available == 1

    response = seller.put('/product/cantaloupe')
    assert response.status_code == 200

    cantaloupe = get_product('cantaloupe')
    assert cantaloupe.available == 2


def test_add_unautorzied(buyer):
    response = buyer.put('/product/cantaloupe')
    assert response.status_code == 401


def test_del(seller):
    assert not get_product('kiwi')
    response = seller.post('/product',
        json = dict(
            name = 'kiwi',
            seller = 'sam',
            cost = 5,
        ),
    )
    assert response.status_code == 201
    response = seller.put('/product/kiwi')
    assert response.status_code == 200
    assert get_product('kiwi').available == 2

    response = seller.delete('/product/kiwi')
    assert response.status_code == 200
    assert get_product('kiwi').available == 1

    response = seller.delete('/product/kiwi')
    assert response.status_code == 200
    assert get_product('kiwi').available == 0

    response = seller.delete('/product/kiwi')
    assert response.status_code == 200
    assert not get_product('kiwi')

    response = seller.delete('/product/kiwi')
    assert response.status_code == 404


def test_del_unautorzied(buyer):
    response = buyer.delete('/product/cantaloupe')
    assert response.status_code == 401


from backend.users import get_user


def test_deposit(buyer):
    buyer.patch('/reset')
    bob = get_user('bob')
    assert bob.deposit == 0

    response = buyer.patch('/deposit/50')
    assert response.status_code == 200
    sold = response.json()
    assert sold == 50
    bob = get_user('bob')
    assert bob.deposit == 50

    response = buyer.patch('/deposit/100')
    assert response.status_code == 200
    sold = response.json()
    assert sold == 150
    bob = get_user('bob')
    assert bob.deposit == 150


def test_deposit_wrong(buyer):
    response = buyer.patch('/deposit/33')
    assert response.status_code == 400


def test_deposit_reset(buyer):
    response = buyer.patch('/reset')
    assert response.status_code == 200
    bob = get_user('bob')
    assert bob.deposit == 0

    response = buyer.patch('/deposit/100')
    assert response.status_code == 200
    bob = get_user('bob')
    assert bob.deposit == 100

    response = buyer.patch('/reset')
    assert response.status_code == 200
    sold = response.json()
    assert sold == 0
    bob = get_user('bob')
    assert bob.deposit == 0



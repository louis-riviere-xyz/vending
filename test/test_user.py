def test_login_invalid(guest):
    response = guest.post('/user/login',
        json = dict(
            username = guest.usr,
            password = guest.psw,
        ),
    )
    assert response.status_code == 401


def test_login(guest, buyer):
    response = guest.post('/user/login',
        json = dict(
            username = buyer.usr,
            password = buyer.psw,
        ),
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_register(guest):
    response = guest.post('/user/login',
        json = dict(
            username = 'joe',
            password = 'joe_password',
        ),
    )
    assert response.status_code == 401

    response = guest.post('/user/register',
        json = dict(
            username  = 'joe',
            password1 = 'joe_password',
            password2 = 'joe_password',
            role      = 'seller',
        ),
    )
    assert response.status_code == 201

    response = guest.post('/user/login',
        json = dict(
            username = 'joe',
            password = 'joe_password',
        ),
    )
    assert response.status_code == 200

    response = guest.post('/user/register',
        json = dict(
            username  = 'joe',
            password1 = 'joe_password',
            password2 = 'joe_password',
            role      = 'seller',
        ),
    )
    assert response.status_code == 400


def test_get_user_unautorized(guest):
    response = guest.get('/user/admin')
    assert response.status_code == 401


def test_get_user(admin):
    response = admin.get('/user/admin')
    assert response.status_code == 200


def test_get_users(admin):
    response = admin.get('/user')
    assert response.status_code == 200


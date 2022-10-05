from fastapi.testclient import TestClient

from pytest import fixture

from rest.api import api


class Client:
    cli = TestClient(api)

    def __init__(self, usr, psw):
        self.usr = usr
        self.psw = psw

    @property
    def token(self):
        if not hasattr(self, '_token'):
            response = self.cli.post('/user/login',
                json = dict(
                    username = self.usr,
                    password = self.psw,
                ),
            )
            json = response.json()
            token = json.get('access_token')
            self._token = token
        return self._token

    @property
    def headers(self):
        headers = dict(
            Authorization = f'Bearer {self.token}',
        )
        return headers

    def add_headers(self, dico):
        headers = dico.pop('headers', {})
        headers.update(self.headers)
        dico['headers'] = headers
        return dico

    def get(self, *a, **k):
        k = self.add_headers(k)
        return self.cli.get(*a, **k)

    def post(self, *a, **k):
        k = self.add_headers(k)
        return self.cli.post(*a, **k)

    def put(self, *a, **k):
        k = self.add_headers(k)
        return self.cli.put(*a, **k)

    def patch(self, *a, **k):
        k = self.add_headers(k)
        return self.cli.patch(*a, **k)

    def delete(self, *a, **k):
        k = self.add_headers(k)
        return self.cli.delete(*a, **k)


@fixture(autouse=True)
def guest():
    return Client('guest', 'na')


@fixture(autouse=True)
def admin():
    return Client('admin', '123456789')


@fixture(autouse=True)
def seller():
    return Client('sam', '123456789')


@fixture(autouse=True)
def buyer():
    return Client('bob', '123456789')


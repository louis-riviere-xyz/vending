from sqlmodel import select

from server import auth
from backend.database import get_session, insert
from backend.model.user import User


def add_user(*, name, role, pswd):
    insert(User(
        username = name,
        password = auth.hash_password(pswd),
        role = role,
    ))


def verify(username, password):
    user = get_user(username)
    verified = auth.verify(password, user.password)
    return verified


def get_user(username):
    with get_session() as session:
        req = select(User).where(
            User.username == username
        )
        return session.exec(req).first()


def get_users():
    with get_session() as session:
        req = select(User)
        return session.exec(req).all()


def get_roles(role):
    return [u.username for u in get_users() if u.role==role]

def get_sellers():
    return get_roles('seller')


def get_buyers():
    return get_roles('buyers')


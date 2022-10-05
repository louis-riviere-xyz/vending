import datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt

from .config import token_timeout


bearer = OAuth2PasswordBearer(tokenUrl='/user/login')

crypt = CryptContext(schemes=['bcrypt'])
secret = 'supersecret'


def hash_password(password):
    return crypt.hash(password)


def verify(pwd, hashed):
    return crypt.verify(pwd, hashed)


def encode(**claims):
    payload = dict(
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=token_timeout),
    )
    payload.update(claims)
    return jwt.encode(payload, secret, algorithm='HS256')


def decode(token):
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired Token')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid Token')


def token(encoded: str = Depends(bearer)):
    decoded = decode(encoded)
    return decoded


def check(token, *authorized):
    role = token['role']
    if role not in authorized:
        raise HTTPException(
            status_code = 401,
            detail      = 'Unauthorized',
        )
    user = token['user']
    return user


def admin(token: str = Depends(token)):
    return check(token, 'admin')

def seller(token: str = Depends(token)):
    return check(token, 'seller')

def buyer(token: str = Depends(token)):
    return check(token, 'buyer')

def anyone(token: str = Depends(token)):
    return check(token, 'buyer', 'seller')

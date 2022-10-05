from os import remove

from sqlmodel import SQLModel, create_engine, Session

from backend.model.user import User
from backend.model.product import Product


db = 'machine.db'


def get_engine():
    return create_engine(f'sqlite:///{db}', echo=False)


def get_session():
    engine = get_engine()
    return Session(engine)


def insert(obj):
    with get_session() as session:
        session.add(obj)
        session.commit()


def update(obj):
    with get_session() as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)


def delete(obj):
    with get_session() as session:
        session.delete(obj)
        session.commit()

def init_db():
    try:
        remove(db)
    except: pass
    engine = get_engine()
    SQLModel.metadata.create_all(engine)



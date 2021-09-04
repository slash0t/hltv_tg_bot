from sqlmodel import Session, select

from utils.db_api.db import engine


def save(obj):
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj


def save_all(objects):
    with Session(engine) as session:
        for obj in objects:
            session.add(obj)

        session.commit()

        for obj in objects:
            session.refresh(obj)

    return objects


def select_by_id(table, pk):
    with Session(engine) as session:
        return session.get(table, pk)


def exec_selection(statement):
    with Session(engine) as session:
        results = session.exec(statement)
        return results


def select_one(statement):
    return exec_selection(statement).one()


def select_first(statement):
    return exec_selection(statement).first()


def select_multiple(statement):
    return exec_selection(statement).all()


def select_all(table):
    statement = select(table)
    return exec_selection(statement).all()

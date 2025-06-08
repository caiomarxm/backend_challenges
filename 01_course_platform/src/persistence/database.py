from collections.abc import Generator
from contextlib import contextmanager

from sqlmodel import Session, create_engine

from src.config.settings import settings

DB_ENGINE = create_engine(settings.DATABASE_CONNECTION_STRING)


@contextmanager
def database_session() -> Generator[Session, None, None]:
    with Session(DB_ENGINE) as session:
        yield session


def get_database_session() -> Generator[Session, None, None]:
    with Session(DB_ENGINE) as session:
        yield session

from sqlmodel import Session, select

from src.exceptions.exceptions import AppError, UserAlreadyExistsErrorDetail
from src.persistence.models import User


def create_user(user_create: User, db_session: Session) -> User:
    select_user_statement = select(User).where(User.email == user_create.email)
    db_user = db_session.exec(select_user_statement).first()

    if db_user:
        print(db_user)
        raise AppError(error_details=UserAlreadyExistsErrorDetail())

    db_user = User(**user_create.model_dump())
    db_session.add(db_user)
    db_session.commit()

    # Refresh db_user to get id value
    db_session.refresh(db_user)

    return db_user


def list_users(db_session: Session, offset: int = 1, limit: int = 10) -> list[User]:
    statement = select(User).offset(offset).limit(limit)
    users = list(db_session.exec(statement).all())

    return users

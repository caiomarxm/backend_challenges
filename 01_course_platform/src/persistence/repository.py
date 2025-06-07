from sqlmodel import Session, col, or_, select

from src.exceptions.exceptions import (
    AppError,
    BadRequestErrorDetail,
    UserAlreadyExistsErrorDetail,
)
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


def list_users(
    db_session: Session,
    offset: int = 1,
    limit: int = 10,
    name: str | None = None,
    email: str | None = None,
) -> list[User]:
    filters = []

    if name:
        filters.append(col(User.full_name).contains(name))

    if email:
        filters.append(col(User.email).contains(email))

    statement = select(User).offset(offset).limit(limit)

    if filters:
        statement = statement.where(or_(*filters))
        print(statement.__repr__)

    users = list(db_session.exec(statement).all())

    return users


def read_user(db_session: Session, user_id: int) -> User | None:
    db_user = db_session.get(User, user_id)

    return db_user


def update_user(db_session: Session, user_id: int, user_update: User) -> User:
    db_user = read_user(db_session, user_id)

    if not db_user:
        raise AppError(
            error_details=BadRequestErrorDetail(error_message="User does not exist")
        )

    # Update the existing user's attributes
    update_data = user_update.model_dump(exclude_none=True, exclude={"id"})
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)

    return db_user

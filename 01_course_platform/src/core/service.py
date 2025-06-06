from src.exceptions.exceptions import (
    AppError,
    BadRequestErrorDetail,
    UserEmailInvalidErrorDetails,
)
from src.http.dtos import UserFilters
from src.persistence import repository
from src.persistence.database import database_session
from src.persistence.models import User, UserBase
from src.utils.validation import is_email_valid


class UserService:
    @staticmethod
    def create_user(user_create: UserBase) -> User:
        db_user = User(**user_create.model_dump())

        if not is_email_valid(user_create.email):
            raise AppError(error_details=UserEmailInvalidErrorDetails())

        with database_session() as session:
            db_user = repository.create_user(db_user, session)

        return db_user

    @staticmethod
    def list_users(filters: UserFilters) -> list[User]:
        if filters.page < 1:
            raise AppError(
                error_details=BadRequestErrorDetail(
                    error_message="Page must be equal or greater than 1"
                )
            )

        if filters.per_page < 1:
            raise AppError(
                error_details=BadRequestErrorDetail(
                    error_message="Per page must be equal or greater than 1"
                )
            )

        offset = filters.per_page * (filters.page - 1)
        limit = filters.per_page

        with database_session() as session:
            users = repository.list_users(
                db_session=session,
                offset=offset,
                limit=limit,
                name=filters.name,
                email=filters.email,
            )

        return users

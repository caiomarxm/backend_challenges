from src.exceptions.exceptions import (
    AppError,
    BadRequestErrorDetail,
    UserEmailInvalidErrorDetails,
)
from src.http.dtos import UpdateUserRequest, UserFilters
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

    @staticmethod
    def update_user(user_id: int, user_update_request: UpdateUserRequest) -> User:
        db_user = None
        with database_session() as session:
            db_user = repository.read_user(session, user_id)

            if not db_user:
                # TODO: Raise specific error here
                raise

            updated_user = db_user.model_copy(
                update=user_update_request.model_dump(exclude_none=True)
            )
            db_user = repository.update_user(
                db_session=session, user_id=user_id, user_update=updated_user
            )

        return db_user

    @staticmethod
    def get_user(user_id: int) -> User:
        with database_session() as session:
            db_user = repository.read_user(db_session=session, user_id=user_id)

        if not db_user:
            raise AppError(
                BadRequestErrorDetail(
                    http_status_code=404, error_message="User does not exist"
                )
            )

        return db_user

    @staticmethod
    def delete_user(user_id: int) -> None:
        with database_session() as session:
            repository.delete_user(db_session=session, user_id=user_id)

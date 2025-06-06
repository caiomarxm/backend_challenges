from src.exceptions.exceptions import AppError, UserEmailInvalidErrorDetails
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

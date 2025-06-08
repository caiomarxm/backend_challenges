from src.exceptions.exceptions import (
    AppError,
    BadRequestErrorDetail,
    UserEmailInvalidErrorDetails,
)
from src.http.dtos import (
    CourseCreate,
    CourseFilters,
    CourseUpdateRequest,
    CourseWithInstructor,
    UpdateUserRequest,
    UserFilters,
    UserWithCoursesInstructed,
)
from src.persistence import repository
from src.persistence.database import database_session
from src.persistence.models import Course, User, UserBase
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
    def get_user(
        user_id: int, include: str | None = None
    ) -> User | UserWithCoursesInstructed:
        with database_session() as session:
            db_user = repository.read_user(db_session=session, user_id=user_id)

            if not db_user:
                raise AppError(
                    BadRequestErrorDetail(
                        http_status_code=404, error_message="User does not exist"
                    )
                )

            if include and "courses_instructed" in include:
                return UserWithCoursesInstructed.model_validate(db_user)

        return db_user

    @staticmethod
    def delete_user(user_id: int) -> None:
        with database_session() as session:
            repository.delete_user(db_session=session, user_id=user_id)


class CourseService:
    @staticmethod
    def create_course(course_create: CourseCreate) -> Course:
        db_course = Course(**course_create.model_dump())

        with database_session() as session:
            db_course = repository.create_course(
                db_session=session, course_create=db_course
            )

        return db_course

    @staticmethod
    def update_course(
        course_id: int, course_update_request: CourseUpdateRequest
    ) -> Course:
        with database_session() as session:
            db_course = Course(**course_update_request.model_dump(exclude_none=True))
            db_course = repository.update_course(
                db_session=session, course_id=course_id, course_update=db_course
            )

        return db_course

    @staticmethod
    def list_courses(
        filters: CourseFilters,
    ) -> list[Course] | list[CourseWithInstructor]:
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
            courses = repository.list_courses(
                db_session=session,
                offset=offset,
                limit=limit,
                name=filters.name,
                description=filters.description,
                instructor_name=filters.instructor_name,
            )

            if filters.include_instructors:
                courses = [
                    CourseWithInstructor(
                        # TODO: As we scale up, we need to make this more performant
                        **course.model_dump(),
                        instructor=course.instructor,
                    )
                    for course in courses
                ]

        return courses

from sqlmodel import Session, and_, col, or_, select

from src.exceptions.exceptions import (
    AppError,
    BadRequestErrorDetail,
    UserAlreadyExistsErrorDetail,
)
from src.persistence.models import Course, Enrollment, User


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


def delete_user(db_session: Session, user_id: int):
    db_user = db_session.get(User, user_id)

    if not db_user:
        raise AppError(
            error_details=BadRequestErrorDetail(
                http_status_code=404, error_message="User does not exist"
            )
        )

    db_session.delete(db_user)
    db_session.commit()


#
# Course
#


def create_course(db_session: Session, course_create: Course) -> Course:
    select_course_statement = select(Course).where(
        and_(
            Course.name == course_create.name,
            Course.instructor_id == course_create.instructor_id,
        )
    )
    db_course = db_session.exec(select_course_statement).first()

    if db_course:
        raise AppError(
            error_details=BadRequestErrorDetail(
                error_message=f"Course {course_create.name} already exists with instructor {db_course.instructor.full_name}"
            )
        )

    db_course = Course(**course_create.model_dump())
    db_session.add(db_course)
    db_session.commit()

    # Refresh db_course to get id value
    db_session.refresh(db_course)

    return db_course


def read_course(db_session: Session, course_id: int) -> Course | None:
    db_course = db_session.get(Course, course_id)

    return db_course


def update_course(db_session: Session, course_id: int, course_update: Course) -> Course:
    db_course = read_course(db_session, course_id)

    if not db_course:
        raise AppError(
            error_details=BadRequestErrorDetail(error_message="Course does not exist")
        )

    # Update the existing user's attributes
    update_data = course_update.model_dump(exclude_none=True, exclude={"id"})
    for key, value in update_data.items():
        setattr(db_course, key, value)

    db_session.add(db_course)
    db_session.commit()
    db_session.refresh(db_course)

    return db_course


def list_courses(
    db_session: Session,
    offset: int = 1,
    limit: int = 10,
    name: str | None = None,
    description: str | None = None,
    instructor_name: str | None = None,
) -> list[Course]:
    filters = []

    if name:
        filters.append(col(Course.name).contains(name))

    if description:
        filters.append(col(Course.description).contains(description))

    if instructor_name:
        select_possible_instructors_statement = select(User).where(
            col(User.full_name).contains(instructor_name)
        )
        possible_instructors = db_session.exec(
            select_possible_instructors_statement
        ).all()
        possible_instructors_ids = [
            instructor.id for instructor in possible_instructors
        ]
        filters.append(col(Course.instructor_id).in_(possible_instructors_ids))

    statement = select(Course).offset(offset).limit(limit)

    if filters:
        statement = statement.where(and_(*filters))
        print(statement.__repr__)

    courses = list(db_session.exec(statement).all())

    return courses


def create_enrollment(db_session: Session, enrollment_create: Enrollment) -> Enrollment:
    user_id = enrollment_create.user_id
    course_id = enrollment_create.course_id

    select_enrollment_statement = select(Enrollment).where(
        and_(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
    )

    db_enrollment = db_session.exec(select_enrollment_statement).first()
    if db_enrollment:
        raise AppError(
            error_details=BadRequestErrorDetail(
                error_message="User is already enrolled in this course"
            )
        )

    db_enrollment = Enrollment(**enrollment_create.model_dump())

    db_session.add(db_enrollment)
    db_session.commit()
    db_session.refresh(db_enrollment)

    return db_enrollment

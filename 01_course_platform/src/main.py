import traceback
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session

from src.config.settings import settings
from src.core.service import CourseService, EnrollmentService, UserService
from src.exceptions.exceptions import AppError
from src.http.dtos import (
    CourseCreate,
    CourseFilters,
    CourseUpdateRequest,
    CreateUserRequest,
    EnrollmentCreate,
    UpdateUserRequest,
    UserFilters,
    UserFull,
    UserWithCoursesEnrolled,
    UserWithCoursesInstructed,
)
from src.persistence.database import get_database_session
from src.persistence.models import User

app = FastAPI()


@app.middleware("http")
async def _render_error_if_request_fails(request: Request, call_next):
    try:
        return await call_next(request)

    except AppError as error:
        print(f"Failed to process user request: {error}")

        error_content = error.detail.model_dump(exclude={"http_status_code"})
        if not settings.DEBUG:
            error_content.pop("debug_message")

        return JSONResponse(
            status_code=error.detail.http_status_code,
            content=error_content,
        )

    except Exception as error:
        trace = traceback.format_exc()
        print(f"Failed to process user request: {error}. Traceback: {trace}")
        return JSONResponse(
            status_code=500,
            content={"detail": "The service could not process your request."},
        )


@app.get("/health")
def _health_check():
    return "Running"


@app.post("/users")
def _create_user(request: CreateUserRequest):
    user = UserService.create_user(user_create=request)

    return user


@app.get("/users")
def _list_users(
    filters: Annotated[UserFilters, Query()],
):
    users = UserService.list_users(filters=filters)

    return users


@app.post("/users/{user_id}")
def _update_user(user_id: int, user: UpdateUserRequest):
    updated_user = UserService.update_user(user_id, user)

    return updated_user


@app.get(
    "/users/{user_id}",
    response_model=User
    | UserWithCoursesInstructed
    | UserWithCoursesEnrolled
    | UserFull,
)
def _get_user(
    user_id: int,
    include: str | None = None,
    db_session: Session = Depends(get_database_session),
):
    user = UserService.get_user(user_id, include=include, db_session=db_session)

    include_courses_instructed = include and "instructed" in include
    include_courses_enrolled = include and "enrolled" in include

    if include_courses_instructed and not include_courses_enrolled:
        return UserWithCoursesInstructed.model_validate(user)

    if not include_courses_instructed and include_courses_enrolled:
        return UserWithCoursesEnrolled.model_validate(user)

    if include_courses_instructed and include_courses_enrolled:
        return UserFull.model_validate(user)

    return user


@app.delete("/users/{user_id}", status_code=204)
def _delete_user(user_id: int):
    UserService.delete_user(user_id=user_id)


#
# Courses
#


@app.post("/courses")
def _create_course(course_create: CourseCreate):
    course = CourseService.create_course(course_create=course_create)

    return course


@app.post("/courses/{course_id}")
def _update_course(course_id: int, course_update: CourseUpdateRequest):
    updated_course = CourseService.update_course(course_id, course_update)

    return updated_course


@app.get("/courses")
def _list_courses(filters: Annotated[CourseFilters, Query()]):
    courses = CourseService.list_courses(filters=filters)

    return courses


@app.post("/enrollments")
def _create_enrollment(enrollment_create: EnrollmentCreate):
    enrollment = EnrollmentService.create_enrollment(
        enrollment_create=enrollment_create
    )

    return enrollment

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel

from src.persistence.models import Course, EnrollmentStatus, User, UserBase


# FIXME: Think if we actually need this
class CreateUserRequest(UserBase):
    pass


class UserFilters(BaseModel):
    email: str | None = None
    name: str | None = None

    page: int = 1
    per_page: int = 10


class UpdateUserRequest(BaseModel):
    email: str | None = None
    full_name: str | None = None


# FIXME: Remove dead code
class CourseResponse(BaseModel):
    id: int | None = None
    name: str
    description: str


class CourseBase(BaseModel):
    name: Annotated[str, "The name of the course"]
    description: Annotated[str, "A brief description of the course"]
    instructor_id: Annotated[int, "The user.id of the instructor of this course"]


class CourseCreate(BaseModel):
    pass


class CourseWithInstructor(CourseBase):
    id: int
    instructor: User


class CourseUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    instructor_id: int | None = None


class UserWithCoursesInstructed(UserBase):
    id: int | None = None
    courses_instructed: list[Course] = []


class CourseFilters(BaseModel):
    name: str | None = None
    description: str | None = None
    instructor_name: str | None = None

    include_instructors: bool = False

    page: int = 1
    per_page: int = 10


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

    start_date: datetime = datetime.now()
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE

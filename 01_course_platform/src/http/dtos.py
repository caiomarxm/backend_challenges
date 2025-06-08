from pydantic import BaseModel

from src.persistence.models import UserBase


# FIXME: Think if we actually need this
class CreateUserRequest(UserBase):
    pass


class UserFilters(BaseModel):
    email: str | None = None
    name: str | None = None

    page: int = 0
    per_page: int = 10


class UpdateUserRequest(BaseModel):
    email: str | None = None
    full_name: str | None = None


class CourseResponse(BaseModel):
    id: int | None = None
    name: str
    description: str


class UserWithCoursesInstructed(UserBase):
    id: int | None = None
    courses_instructed: list[CourseResponse] = []

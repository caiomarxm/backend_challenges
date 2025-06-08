from datetime import datetime
from enum import Enum

from sqlalchemy import null
from sqlmodel import Field, Relationship, SQLModel


class EnrollmentStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"


class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"  # type: ignore

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    course_id: int = Field(foreign_key="courses.id", primary_key=True)

    start_date: datetime = Field(default_factory=datetime.now)
    status: EnrollmentStatus


class UserBase(SQLModel):
    email: str
    full_name: str | None = None


class User(UserBase, table=True):
    __tablename__ = "users"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    email: str = Field(unique=True, index=True)
    full_name: str | None = None

    courses_instructed: list["Course"] = Relationship(back_populates="instructor")

    courses_enrolled: list["Course"] = Relationship(
        back_populates="students", link_model=Enrollment
    )


class Course(SQLModel, table=True):
    __tablename__ = "courses"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    name: str
    description: str

    instructor_id: int = Field(foreign_key="users.id")
    instructor: User = Relationship(back_populates="courses_instructed")

    students: list[User] = Relationship(
        back_populates="courses_enrolled", link_model=Enrollment
    )

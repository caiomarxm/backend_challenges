from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: str
    full_name: str | None = None


class User(UserBase, table=True):
    __tablename__ = "users"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    email: str = Field(unique=True, index=True)
    full_name: str | None = None

    courses_instructed: list["Course"] = Relationship(back_populates="instructor")


class Course(SQLModel, table=True):
    __tablename__ = "courses"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    name: str
    description: str

    instructor_id: int = Field(foreign_key="users.id")
    instructor: User = Relationship(back_populates="courses_instructed")

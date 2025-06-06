from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str
    full_name: str | None = None


class User(UserBase, table=True):
    __tablename__ = "users"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    email: str = Field(unique=True, index=True)
    full_name: str | None = None

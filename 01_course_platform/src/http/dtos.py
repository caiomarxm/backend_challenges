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

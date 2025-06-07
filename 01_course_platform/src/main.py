import traceback
from typing import Annotated

from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.core.service import UserService
from src.exceptions.exceptions import AppError
from src.http.dtos import CreateUserRequest, UpdateUserRequest, UserFilters

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
def _list_users(filters: Annotated[UserFilters, Query()]):
    users = UserService.list_users(filters=filters)

    return users


@app.post("/users/{user_id}")
def _update_user(user_id: int, user: UpdateUserRequest):
    updated_user = UserService.update_user(user_id, user)

    return updated_user


@app.get("/users/{user_id}")
def _get_user(user_id: int):
    return UserService.get_user(user_id)

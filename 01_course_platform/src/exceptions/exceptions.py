from enum import Enum

from pydantic import BaseModel


class ErrorCode(str, Enum):
    BAD_REQUEST = "bad_request"

    USER_ALREADY_EXISTS = "user_already_exists"
    USER_EMAIL_INVALID = "user_email_invalid"


class ErrorDetail(BaseModel):
    error_code: ErrorCode
    http_status_code: int
    error_message: str

    # TODO: Don't propagate this to the frontend
    debug_message: str | None = None


class BadRequestErrorDetail(ErrorDetail):
    error_code: ErrorCode = ErrorCode.BAD_REQUEST
    http_status_code: int = 400
    error_message: str


class UserAlreadyExistsErrorDetail(ErrorDetail):
    error_code: ErrorCode = ErrorCode.USER_ALREADY_EXISTS
    http_status_code: int = 400
    error_message: str = "A user with this email already exists in the platform"


class UserEmailInvalidErrorDetails(ErrorDetail):
    error_code: ErrorCode = ErrorCode.USER_EMAIL_INVALID
    http_status_code: int = 400
    error_message: str = "The provided email is invalid"


class AppError(Exception):
    detail: ErrorDetail

    def __init__(self, error_details: ErrorDetail):
        self.detail = error_details

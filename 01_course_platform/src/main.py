import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.exceptions.exceptions import AppError

app = FastAPI()


@app.middleware("http")
async def _render_error_if_request_fails(request: Request, call_next):
    try:
        return await call_next(request)

    except AppError as error:
        print(f"Failed to process user request: {error}")

        error_content = error.detail.model_dump()
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

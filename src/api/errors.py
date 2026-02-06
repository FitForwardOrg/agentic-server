from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    message: str
    code: str | None = None
    field: str | None = None


class ErrorResponse(BaseModel):
    success: bool = Field(default=False)
    error: ErrorDetail


class AppError(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, code: str | None = None):
        self.message = message
        self.status_code = status_code
        self.code = code


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found", code: str = "NOT_FOUND"):
        super().__init__(message, status.HTTP_404_NOT_FOUND, code)


class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed", code: str = "VALIDATION_ERROR"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, code)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized access", code: str = "UNAUTHORIZED"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, code)


async def app_exception_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=ErrorDetail(message=exc.message, code=exc.code)).model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error=ErrorDetail(message="An unexpected error occurred", code="INTERNAL_SERVER_ERROR")
        ).model_dump(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(
                message=exc.detail if isinstance(exc.detail, str) else str(exc.detail),
                code="NOT_FOUND" if exc.status_code == status.HTTP_404_NOT_FOUND else "HTTP_EXCEPTION",
            )
        ).model_dump(),
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppError, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

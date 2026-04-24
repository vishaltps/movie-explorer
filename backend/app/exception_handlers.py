"""Four-layer exception handler chain. Every error becomes a uniform Envelope response."""

import structlog
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import AppError
from app.schemas.envelope import Envelope, ErrorPayload, Meta

logger = structlog.get_logger(__name__)


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None) or request.headers.get("X-Request-ID")


def _error_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
    details: dict[str, object] | None = None,
) -> JSONResponse:
    rid = _request_id(request)
    body = Envelope[None](
        success=False,
        error=ErrorPayload(code=code, message=message, details=details),
        meta=Meta(request_id=rid),
    ).model_dump(exclude_none=True)
    return JSONResponse(status_code=status_code, content=body)


async def app_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle domain AppError subclasses (NotFoundError, BadRequestError, etc.)."""
    err = exc if isinstance(exc, AppError) else AppError(str(exc))
    return _error_response(
        request,
        status_code=err.status_code,
        code=err.code,
        message=err.message,
        details=err.details,
    )


async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle Pydantic RequestValidationError — returns 422 with field-level details."""
    assert isinstance(exc, RequestValidationError)
    return _error_response(
        request,
        status_code=422,
        code="validation_error",
        message="Request validation failed",
        details={"fields": exc.errors()},
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Wrap FastAPI/Starlette HTTP exceptions in the envelope."""
    assert isinstance(exc, StarletteHTTPException)
    return _error_response(
        request,
        status_code=exc.status_code,
        code=f"http_{exc.status_code}",
        message=str(exc.detail),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all: log full traceback, return a generic 500. Never leaks internals."""
    rid = _request_id(request)
    logger.exception(
        "unhandled_exception",
        request_id=rid,
        path=request.url.path,
        method=request.method,
        error_type=type(exc).__name__,
    )
    return _error_response(
        request,
        status_code=500,
        code="internal_error",
        message="An unexpected error occurred",
    )

"""Domain exception hierarchy for consistent API error handling."""
from typing import Any


class AppError(Exception):
    """Base error for all application-level issues."""

    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class NotFoundError(AppError):
    """Raised when a resource (Movie, Actor, etc.) is not found."""
    status_code = 404
    code = "not_found"


class BadRequestError(AppError):
    """Raised for invalid input or failed business logic validation."""
    status_code = 400
    code = "bad_request"


class ConflictError(AppError):
    """Raised when an operation conflicts with existing data."""
    status_code = 409
    code = "conflict"
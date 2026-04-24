"""Uniform response envelope used by every endpoint and exception handler."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ErrorPayload(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class Meta(BaseModel):
    request_id: str | None = None
    pagination: PaginationMeta | None = None


class Envelope(BaseModel, Generic[T]):
    """Every API response — success or failure — uses this shape."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool
    data: T | None = None
    error: ErrorPayload | None = None
    meta: Meta | None = None

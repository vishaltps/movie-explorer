"""Shared data-service helpers: pagination, sort whitelist, success envelope builder."""
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db import Base
from app.exceptions import NotFoundError
from app.schemas.envelope import Envelope, Meta, PaginationMeta


def paginate(
    db: Session,
    stmt: Select[Any],
    page: int,
    page_size: int,
) -> tuple[list[Any], PaginationMeta]:
    """Run count + page queries. Returns items and page-based metadata."""
    count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
    total = int(db.scalar(count_stmt) or 0)
    items = list(db.scalars(stmt.limit(page_size).offset((page - 1) * page_size)).all())
    total_pages = (total + page_size - 1) // page_size if total else 0
    return items, PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages)


def ok(
    data: Any,
    *,
    pagination: PaginationMeta | None = None,
    request_id: str | None = None,
) -> Envelope[Any]:
    """Build a success envelope."""
    return Envelope(
        success=True,
        data=data,
        meta=Meta(request_id=request_id, pagination=pagination),
    )


class BaseService[T: Base]:
    def __init__(self, model: type[T]) -> None:
        self.model = model

    def get_by_id(self, db: Session, item_id: int) -> T:
        obj = db.get(self.model, item_id)
        if obj is None:
            raise NotFoundError(f"{self.model.__name__} with id {item_id} not found")
        return obj

    def paginate(
        self, db: Session, stmt: Select[tuple[T]], page: int, page_size: int
    ) -> tuple[list[T], PaginationMeta]:
        count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
        total = int(db.scalar(count_stmt) or 0)
        rows = list(db.scalars(stmt.limit(page_size).offset((page - 1) * page_size)).all())
        total_pages = (total + page_size - 1) // page_size if total else 0
        return rows, PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages)

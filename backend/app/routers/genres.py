from typing import Any

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.data_services.base import ok
from app.data_services.genre_service import GenreService
from app.db import get_db
from app.schemas.envelope import Envelope
from app.schemas.genre import GenreOut

router = APIRouter(prefix="/api/v1/genres", tags=["Genres"])
service = GenreService()


@router.get("", response_model=Envelope[dict[str, Any]])
def list_genres(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Envelope[dict[str, Any]]:
    items, pagination = service.list(db, page=page, page_size=page_size)
    return ok(
        {"items": [GenreOut.model_validate(item).model_dump() for item in items]},
        pagination=pagination,
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{genre_id}", response_model=Envelope[GenreOut])
def get_genre(genre_id: int, request: Request, db: Session = Depends(get_db)) -> Envelope[GenreOut]:
    return ok(
        GenreOut.model_validate(service.get_by_id(db, genre_id)),
        request_id=getattr(request.state, "request_id", None),
    )

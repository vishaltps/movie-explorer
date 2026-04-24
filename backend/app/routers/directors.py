from typing import Any

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.data_services.base import ok
from app.data_services.director_service import DirectorService
from app.db import get_db
from app.schemas.director import DirectorOut
from app.schemas.envelope import Envelope

router = APIRouter(prefix="/api/v1/directors", tags=["Directors"])
service = DirectorService()


@router.get("", response_model=Envelope[dict[str, Any]])
def list_directors(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Envelope[dict[str, Any]]:
    items, pagination = service.list(db, page=page, page_size=page_size)
    return ok(
        {"items": [DirectorOut.model_validate(item).model_dump() for item in items]},
        pagination=pagination,
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{director_id}", response_model=Envelope[DirectorOut])
def get_director(director_id: int, request: Request, db: Session = Depends(get_db)) -> Envelope[DirectorOut]:
    return ok(
        DirectorOut.model_validate(service.get_by_id(db, director_id)),
        request_id=getattr(request.state, "request_id", None),
    )

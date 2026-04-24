from typing import Any

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.data_services.actor_service import ActorService
from app.data_services.base import ok
from app.db import get_db
from app.schemas.actor import ActorOut
from app.schemas.envelope import Envelope

router = APIRouter(prefix="/api/v1/actors", tags=["Actors"])
service = ActorService()


@router.get("", response_model=Envelope[dict[str, Any]])
def list_actors(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    genre_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> Envelope[dict[str, Any]]:
    items, pagination = service.list(db, page=page, page_size=page_size, genre_id=genre_id)
    return ok(
        {"items": [ActorOut.model_validate(item).model_dump() for item in items]},
        pagination=pagination,
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{actor_id}", response_model=Envelope[ActorOut])
def get_actor(actor_id: int, request: Request, db: Session = Depends(get_db)) -> Envelope[ActorOut]:
    return ok(
        ActorOut.model_validate(service.get_by_id(db, actor_id)),
        request_id=getattr(request.state, "request_id", None),
    )

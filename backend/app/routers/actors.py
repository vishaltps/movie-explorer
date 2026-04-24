"""Actor endpoints."""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.data_services.actor_service import ActorService
from app.data_services.base import ok
from app.db import get_db
from app.schemas.actor import ActorDetail, ActorFilters, ActorRead
from app.schemas.envelope import Envelope
from app.schemas.movie import MovieRead

router = APIRouter(prefix="/api/v1/actors", tags=["Actors"])
service = ActorService()


@router.get("", response_model=Envelope[list[ActorRead]], summary="List actors")
def list_actors(
    request: Request,
    filters: ActorFilters = Depends(),
    db: Session = Depends(get_db),
) -> Envelope[list[ActorRead]]:
    items, pagination = service.list(db, filters)
    return ok([ActorRead.model_validate(a) for a in items], pagination=pagination,
              request_id=getattr(request.state, "request_id", None))


@router.get("/{actor_id}", response_model=Envelope[ActorDetail], summary="Get actor by ID")
def get_actor(actor_id: int, request: Request, db: Session = Depends(get_db)) -> Envelope[ActorDetail]:
    return ok(ActorDetail.model_validate(service.get_by_id(db, actor_id)),
              request_id=getattr(request.state, "request_id", None))


@router.get("/{actor_id}/movies", response_model=Envelope[list[MovieRead]], summary="Movies by actor")
def list_actor_movies(
    actor_id: int,
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Envelope[list[MovieRead]]:
    items, pagination = service.get_actor_movies(db, actor_id, page, page_size)
    return ok([MovieRead.model_validate(m) for m in items], pagination=pagination,
              request_id=getattr(request.state, "request_id", None))

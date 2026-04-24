"""Director endpoints."""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.data_services.base import ok
from app.data_services.director_service import DirectorService
from app.db import get_db
from app.schemas.director import DirectorDetail, DirectorFilters, DirectorRead
from app.schemas.envelope import Envelope
from app.schemas.movie import MovieRead

router = APIRouter(prefix="/api/v1/directors", tags=["Directors"])
service = DirectorService()


@router.get("", response_model=Envelope[list[DirectorRead]], summary="List directors")
def list_directors(
    request: Request,
    filters: DirectorFilters = Depends(),
    db: Session = Depends(get_db),
) -> Envelope[list[DirectorRead]]:
    items, pagination = service.list(db, filters)
    return ok([DirectorRead.model_validate(d) for d in items], pagination=pagination,
              request_id=getattr(request.state, "request_id", None))


@router.get("/{director_id}", response_model=Envelope[DirectorDetail], summary="Get director by ID")
def get_director(director_id: int, request: Request, db: Session = Depends(get_db)) -> Envelope[DirectorDetail]:
    return ok(DirectorDetail.model_validate(service.get_by_id(db, director_id)),
              request_id=getattr(request.state, "request_id", None))


@router.get("/{director_id}/movies", response_model=Envelope[list[MovieRead]], summary="Movies by director")
def list_director_movies(
    director_id: int,
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Envelope[list[MovieRead]]:
    items, pagination = service.get_director_movies(db, director_id, page, page_size)
    return ok([MovieRead.model_validate(m) for m in items], pagination=pagination,
              request_id=getattr(request.state, "request_id", None))

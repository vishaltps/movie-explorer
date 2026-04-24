"""Movie endpoints — the central resource."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.data_services.base import ok
from app.data_services.movie_service import MovieService
from app.db import get_db
from app.schemas.envelope import Envelope
from app.schemas.movie import MovieDetail, MovieFilters, MovieRead

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])
service = MovieService()


@router.get("", response_model=Envelope[list[MovieRead]], summary="List movies with filters")
def list_movies(
    request: Request,
    filters: MovieFilters = Depends(),
    db: Session = Depends(get_db),
) -> Envelope[list[MovieRead]]:
    items, pagination = service.list(db, filters)
    return ok(
        [MovieRead.model_validate(m) for m in items],
        pagination=pagination,
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{movie_id}", response_model=Envelope[MovieDetail], summary="Get movie by ID")
def get_movie(
    movie_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> Envelope[MovieDetail]:
    return ok(
        MovieDetail.model_validate(service.get_detail(db, movie_id)),
        request_id=getattr(request.state, "request_id", None),
    )

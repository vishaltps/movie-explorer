from typing import Any

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.data_services.base import ok
from app.data_services.movie_service import MovieService
from app.db import get_db
from app.schemas.envelope import Envelope
from app.schemas.movie import MovieDetailOut, MovieListItemOut

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])
service = MovieService()


@router.get("", response_model=Envelope[dict[str, Any]])
def list_movies(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    q: str | None = Query(default=None),
    genre_id: int | None = Query(default=None),
    director_id: int | None = Query(default=None),
    actor_id: int | None = Query(default=None),
    min_year: int | None = Query(default=None),
    max_year: int | None = Query(default=None),
    sort: str = Query(default="title"),
    db: Session = Depends(get_db),
) -> Envelope[dict[str, Any]]:
    items, pagination = service.list(
        db,
        page=page,
        page_size=page_size,
        q=q,
        genre_id=genre_id,
        director_id=director_id,
        actor_id=actor_id,
        min_year=min_year,
        max_year=max_year,
        sort=sort,
    )
    return ok(
        {"items": [MovieListItemOut.model_validate(item).model_dump() for item in items]},
        pagination=pagination,
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{movie_id}", response_model=Envelope[MovieDetailOut])
def get_movie(movie_id: int, request: Request, db: Session = Depends(get_db)) -> Envelope[MovieDetailOut]:
    return ok(
        MovieDetailOut.model_validate(service.get_detail(db, movie_id)),
        request_id=getattr(request.state, "request_id", None),
    )

"""Genre endpoints."""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.data_services.base import ok
from app.data_services.genre_service import GenreService
from app.db import get_db
from app.schemas.envelope import Envelope
from app.schemas.genre import GenreRead

router = APIRouter(prefix="/api/v1/genres", tags=["Genres"])
service = GenreService()


@router.get("", response_model=Envelope[list[GenreRead]], summary="List all genres")
def list_genres(request: Request, db: Session = Depends(get_db)) -> Envelope[list[GenreRead]]:
    """Return all genres. Small dataset — no pagination."""
    items = service.list_all(db)
    return ok([GenreRead.model_validate(g) for g in items],
              request_id=getattr(request.state, "request_id", None))


@router.get("/{genre_id}", response_model=Envelope[GenreRead], summary="Get genre by ID")
def get_genre(genre_id: int, request: Request, db: Session = Depends(get_db)) -> Envelope[GenreRead]:
    return ok(GenreRead.model_validate(service.get_by_id(db, genre_id)),
              request_id=getattr(request.state, "request_id", None))


@router.get("/{genre_id}/movies", summary="List movies in a genre")
def list_genre_movies(
    genre_id: int,
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Envelope[list]:
    from app.data_services.movie_service import MovieService
    from app.schemas.movie import MovieFilters, MovieRead
    movie_svc = MovieService()
    items, pagination = movie_svc.list(db, MovieFilters(genre_id=genre_id, page=page, page_size=page_size))
    return ok([MovieRead.model_validate(m) for m in items], pagination=pagination,
              request_id=getattr(request.state, "request_id", None))

"""Reviews endpoint — nested under /movies/{movie_id}/reviews."""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.data_services.base import ok
from app.data_services.review_service import ReviewService
from app.db import get_db
from app.schemas.envelope import Envelope
from app.schemas.review import ReviewRead

router = APIRouter(prefix="/api/v1/movies/{movie_id}/reviews", tags=["Reviews"])
service = ReviewService()


@router.get("", response_model=Envelope[list[ReviewRead]], summary="List reviews for a movie")
def list_reviews(
    movie_id: int,
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Envelope[list[ReviewRead]]:
    items, pagination = service.list_for_movie(db, movie_id=movie_id, page=page, page_size=page_size)
    return ok([ReviewRead.model_validate(r) for r in items], pagination=pagination,
              request_id=getattr(request.state, "request_id", None))

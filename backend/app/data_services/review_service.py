"""Review data service — read-only, scoped to a movie."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_services.base import BaseService
from app.exceptions import NotFoundError
from app.models.movie import Movie
from app.models.review import Review
from app.schemas.envelope import PaginationMeta


class ReviewService(BaseService[Review]):
    def __init__(self) -> None:
        super().__init__(Review)

    def list_for_movie(
        self, db: Session, movie_id: int, page: int, page_size: int
    ) -> tuple[list[Review], PaginationMeta]:
        if db.get(Movie, movie_id) is None:
            raise NotFoundError(f"Movie {movie_id} not found")
        stmt = select(Review).where(Review.movie_id == movie_id).order_by(Review.created_at.desc())
        return self.paginate(db, stmt, page, page_size)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_services.base import BaseService
from app.models.review import Review
from app.schemas.envelope import PaginationMeta


class ReviewService(BaseService[Review]):
    def __init__(self) -> None:
        super().__init__(Review)

    def list_for_movie(
        self, db: Session, movie_id: int, page: int, page_size: int
    ) -> tuple[list[Review], PaginationMeta]:
        stmt = select(Review).where(Review.movie_id == movie_id).order_by(Review.id.asc())
        return self.paginate(db, stmt, page, page_size)

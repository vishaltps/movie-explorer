from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_services.base import BaseService
from app.models.genre import Genre
from app.schemas.envelope import PaginationMeta


class GenreService(BaseService[Genre]):
    def __init__(self) -> None:
        super().__init__(Genre)

    def list(self, db: Session, page: int, page_size: int) -> tuple[list[Genre], PaginationMeta]:
        stmt = select(Genre).order_by(Genre.name.asc())
        return self.paginate(db, stmt, page, page_size)

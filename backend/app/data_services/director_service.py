from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_services.base import BaseService
from app.models.director import Director
from app.schemas.envelope import PaginationMeta


class DirectorService(BaseService[Director]):
    def __init__(self) -> None:
        super().__init__(Director)

    def list(self, db: Session, page: int, page_size: int) -> tuple[list[Director], PaginationMeta]:
        stmt = select(Director).order_by(Director.name.asc())
        return self.paginate(db, stmt, page, page_size)

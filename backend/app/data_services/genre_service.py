from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_services.base import BaseService
from app.models.genre import Genre


class GenreService(BaseService[Genre]):
    def __init__(self) -> None:
        super().__init__(Genre)

    def list_all(self, db: Session) -> list[Genre]:
        """Return all genres sorted by name. No pagination — genre set is small."""
        return list(db.scalars(select(Genre).order_by(Genre.name.asc())).all())

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.data_services.base import BaseService
from app.models.actor import Actor
from app.models.movie import Movie
from app.schemas.envelope import PaginationMeta


class ActorService(BaseService[Actor]):
    def __init__(self) -> None:
        super().__init__(Actor)

    def list(
        self, db: Session, page: int, page_size: int, genre_id: int | None = None
    ) -> tuple[list[Actor], PaginationMeta]:
        stmt: Select[tuple[Actor]] = select(Actor).order_by(Actor.name.asc())
        if genre_id is not None:
            stmt = stmt.join(Actor.movies).where(Movie.genre_id == genre_id).distinct()
        return self.paginate(db, stmt, page, page_size)

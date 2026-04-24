from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from app.data_services.base import BaseService
from app.models.movie import Movie
from app.schemas.envelope import PaginationMeta


class MovieService(BaseService[Movie]):
    def __init__(self) -> None:
        super().__init__(Movie)

    def list(
        self,
        db: Session,
        page: int,
        page_size: int,
        q: str | None = None,
        genre_id: int | None = None,
        director_id: int | None = None,
        actor_id: int | None = None,
        min_year: int | None = None,
        max_year: int | None = None,
        sort: str = "title",
    ) -> tuple[list[Movie], PaginationMeta]:
        stmt: Select[tuple[Movie]] = select(Movie).options(
            selectinload(Movie.genre), selectinload(Movie.director), selectinload(Movie.actors)
        )
        if q:
            stmt = stmt.where(Movie.title.ilike(f"%{q}%"))
        if genre_id is not None:
            stmt = stmt.where(Movie.genre_id == genre_id)
        if director_id is not None:
            stmt = stmt.where(Movie.director_id == director_id)
        if actor_id is not None:
            stmt = stmt.join(Movie.actors).where(Movie.actors.any(id=actor_id)).distinct()
        if min_year is not None:
            stmt = stmt.where(Movie.year >= min_year)
        if max_year is not None:
            stmt = stmt.where(Movie.year <= max_year)

        if sort == "-year":
            stmt = stmt.order_by(Movie.year.desc(), Movie.title.asc())
        elif sort == "year":
            stmt = stmt.order_by(Movie.year.asc(), Movie.title.asc())
        elif sort == "-rating":
            stmt = stmt.order_by(Movie.rating.desc(), Movie.title.asc())
        elif sort == "rating":
            stmt = stmt.order_by(Movie.rating.asc(), Movie.title.asc())
        else:
            stmt = stmt.order_by(Movie.title.asc())

        return self.paginate(db, stmt, page, page_size)

    def get_detail(self, db: Session, movie_id: int) -> Movie:
        stmt = (
            select(Movie)
            .where(Movie.id == movie_id)
            .options(
                selectinload(Movie.genre),
                selectinload(Movie.director),
                selectinload(Movie.actors),
            )
        )
        movie = db.scalars(stmt).first()
        if movie is None:
            return self.get_by_id(db, movie_id)
        return movie

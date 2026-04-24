"""Movie data service — list with composable filters, detail with eager loading."""
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.data_services.base import BaseService
from app.models.actor import Actor
from app.models.genre import Genre
from app.models.movie import Movie
from app.schemas.envelope import PaginationMeta
from app.schemas.movie import MovieFilters


class MovieService(BaseService[Movie]):
    def __init__(self) -> None:
        super().__init__(Movie)

    def list(self, db: Session, f: MovieFilters) -> tuple[list[Movie], PaginationMeta]:
        stmt = select(Movie).options(
            selectinload(Movie.genres),
            selectinload(Movie.director),
        )
        if f.genre_id is not None:
            stmt = stmt.join(Movie.genres).where(Genre.id == f.genre_id)
        if f.director_id is not None:
            stmt = stmt.where(Movie.director_id == f.director_id)
        if f.actor_id is not None:
            stmt = stmt.join(Movie.actors).where(Actor.id == f.actor_id)
        if f.year is not None:
            stmt = stmt.where(Movie.release_year == f.year)
        if f.year_min is not None:
            stmt = stmt.where(Movie.release_year >= f.year_min)
        if f.year_max is not None:
            stmt = stmt.where(Movie.release_year <= f.year_max)
        if f.search:
            stmt = stmt.where(Movie.title.ilike(f"%{f.search}%"))
        if f.genre_id is not None or f.actor_id is not None:
            stmt = stmt.distinct()

        # Apply sort
        if f.sort == "-release_year":
            stmt = stmt.order_by(Movie.release_year.desc(), Movie.title.asc())
        elif f.sort == "release_year":
            stmt = stmt.order_by(Movie.release_year.asc(), Movie.title.asc())
        elif f.sort == "-average_rating":
            stmt = stmt.order_by(Movie.average_rating.desc().nulls_last(), Movie.title.asc())
        elif f.sort == "average_rating":
            stmt = stmt.order_by(Movie.average_rating.asc().nulls_last(), Movie.title.asc())
        else:
            stmt = stmt.order_by(Movie.title.asc())

        return self.paginate(db, stmt, f.page, f.page_size)

    def get_detail(self, db: Session, movie_id: int) -> Movie:
        stmt = (
            select(Movie)
            .where(Movie.id == movie_id)
            .options(
                selectinload(Movie.genres),
                selectinload(Movie.director),
                selectinload(Movie.actors),
                selectinload(Movie.reviews),
            )
        )
        movie = db.scalars(stmt).first()
        if movie is None:
            return self.get_by_id(db, movie_id)  # raises NotFoundError
        return movie

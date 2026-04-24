"""Actor data service — list with filters including the actors-by-genre join."""

from __future__ import annotations

import builtins

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_services.base import BaseService
from app.models.actor import Actor
from app.models.genre import Genre
from app.models.movie import Movie
from app.schemas.actor import ActorFilters
from app.schemas.envelope import PaginationMeta


class ActorService(BaseService[Actor]):
    def __init__(self) -> None:
        super().__init__(Actor)

    def list(self, db: Session, f: ActorFilters) -> tuple[list[Actor], PaginationMeta]:
        stmt = select(Actor).order_by(Actor.name.asc())
        if f.movie_id is not None:
            stmt = stmt.join(Actor.movies).where(Movie.id == f.movie_id)
        if f.genre_id is not None:
            # Actors who appeared in at least one movie of this genre (M2M join)
            stmt = stmt.join(Actor.movies).join(Movie.genres).where(Genre.id == f.genre_id)
        if f.search:
            stmt = stmt.where(Actor.name.ilike(f"%{f.search}%"))
        if f.movie_id is not None or f.genre_id is not None:
            stmt = stmt.distinct()
        return self.paginate(db, stmt, f.page, f.page_size)

    def get_actor_movies(
        self, db: Session, actor_id: int, page: int, page_size: int
    ) -> tuple[builtins.list[Movie], PaginationMeta]:
        self.get_by_id(db, actor_id)  # raises NotFoundError if missing
        from sqlalchemy import select as sa_select

        stmt = (
            sa_select(Movie)
            .join(Movie.actors)
            .where(Actor.id == actor_id)
            .order_by(Movie.release_year.desc())
        )
        from app.data_services.base import paginate as standalone_paginate

        return standalone_paginate(db, stmt, page, page_size)

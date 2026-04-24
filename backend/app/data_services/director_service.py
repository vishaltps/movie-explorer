"""Director data service."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_services.base import BaseService
from app.models.director import Director
from app.models.movie import Movie
from app.schemas.director import DirectorFilters
from app.schemas.envelope import PaginationMeta


class DirectorService(BaseService[Director]):
    def __init__(self) -> None:
        super().__init__(Director)

    def list(self, db: Session, f: DirectorFilters) -> tuple[list[Director], PaginationMeta]:
        stmt = select(Director).order_by(Director.name.asc())
        if f.search:
            stmt = stmt.where(Director.name.ilike(f"%{f.search}%"))
        return self.paginate(db, stmt, f.page, f.page_size)

    def get_director_movies(
        self, db: Session, director_id: int, page: int, page_size: int
    ) -> tuple[list[Movie], PaginationMeta]:
        self.get_by_id(db, director_id)  # raises NotFoundError if missing
        stmt = (
            select(Movie)
            .where(Movie.director_id == director_id)
            .order_by(Movie.release_year.desc())
        )
        from app.data_services.base import paginate as standalone_paginate
        return standalone_paginate(db, stmt, page, page_size)

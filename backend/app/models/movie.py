from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.associations import movie_actors, movie_genres

if TYPE_CHECKING:
    from app.models.actor import Actor
    from app.models.director import Director
    from app.models.genre import Genre
    from app.models.review import Review


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    release_year: Mapped[int] = mapped_column(nullable=False, index=True)
    synopsis: Mapped[str | None] = mapped_column(Text, nullable=True)
    poster_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    runtime_minutes: Mapped[int | None] = mapped_column(nullable=True)
    director_id: Mapped[int | None] = mapped_column(
        ForeignKey("directors.id", ondelete="SET NULL"), nullable=True, index=True
    )
    average_rating: Mapped[float | None] = mapped_column(Float, nullable=True)

    director: Mapped[Director | None] = relationship("Director", back_populates="movies")
    genres: Mapped[list[Genre]] = relationship(
        "Genre", secondary=movie_genres, back_populates="movies", lazy="selectin"
    )
    actors: Mapped[list[Actor]] = relationship(
        "Actor", secondary=movie_actors, back_populates="movies", lazy="selectin"
    )
    reviews: Mapped[list[Review]] = relationship(
        "Review", back_populates="movie", cascade="all, delete-orphan", lazy="selectin"
    )

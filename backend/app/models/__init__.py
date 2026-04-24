"""Import all models so SQLAlchemy registers them before Alembic or Base.metadata operations."""

from app.models.actor import Actor
from app.models.associations import movie_actors, movie_genres
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.review import Review

__all__ = ["Actor", "Director", "Genre", "Movie", "Review", "movie_actors", "movie_genres"]

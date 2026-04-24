from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.actor import ActorRead
from app.schemas.director import DirectorRead
from app.schemas.genre import GenreRead
from app.schemas.review import ReviewRead


class MovieRead(BaseModel):
    """Compact view for movie lists — includes genres and director for card display."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    release_year: int
    poster_url: str | None = None
    average_rating: float | None = None
    genres: list[GenreRead] = []
    director: DirectorRead | None = None


class MovieDetail(MovieRead):
    """Full detail view — adds synopsis, runtime, cast, and reviews."""
    synopsis: str | None = None
    runtime_minutes: int | None = None
    actors: list[ActorRead] = []
    reviews: list[ReviewRead] = []


class MovieFilters(BaseModel):
    genre_id: int | None = Field(default=None, gt=0)
    director_id: int | None = Field(default=None, gt=0)
    actor_id: int | None = Field(default=None, gt=0)
    year: int | None = Field(default=None, ge=1888, le=2100)
    year_min: int | None = Field(default=None, ge=1888, le=2100)
    year_max: int | None = Field(default=None, ge=1888, le=2100)
    search: str | None = Field(default=None, max_length=200)
    sort: str | None = Field(
        default=None, pattern=r"^-?(title|release_year|average_rating)$"
    )
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @model_validator(mode="after")
    def check_year_range(self) -> "MovieFilters":
        if (
            self.year_min is not None
            and self.year_max is not None
            and self.year_min > self.year_max
        ):
            raise ValueError("year_min cannot be greater than year_max")
        return self

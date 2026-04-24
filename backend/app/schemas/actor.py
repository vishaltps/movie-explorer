from pydantic import BaseModel, ConfigDict, Field


class ActorRead(BaseModel):
    """Compact view — used in lists and embedded in MovieDetail."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    birth_year: int | None = None


class ActorDetail(ActorRead):
    """Full view with bio."""

    bio: str | None = None


class ActorFilters(BaseModel):
    movie_id: int | None = Field(default=None, gt=0)
    genre_id: int | None = Field(default=None, gt=0)
    search: str | None = Field(default=None, max_length=200)
    sort: str | None = Field(default=None, pattern=r"^-?(name)$")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

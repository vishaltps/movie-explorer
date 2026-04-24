from pydantic import BaseModel, ConfigDict, Field


class DirectorRead(BaseModel):
    """Compact view — embedded in movie list and movie detail."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    birth_year: int | None = None


class DirectorDetail(DirectorRead):
    """Full view with bio. Returned on /directors/{id}."""

    bio: str | None = None


class DirectorFilters(BaseModel):
    search: str | None = Field(default=None, max_length=200)
    sort: str | None = Field(default=None, pattern=r"^-?(name)$")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

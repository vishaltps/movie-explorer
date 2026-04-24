from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    movie_id: int
    author_name: str
    rating: int
    comment: str
    created_at: datetime

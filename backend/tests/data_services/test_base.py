import pytest

from app.data_services.genre_service import GenreService
from app.exceptions import NotFoundError


def test_get_by_id_raises_not_found(db_session):
    service = GenreService()
    with pytest.raises(NotFoundError):
        service.get_by_id(db_session, 999)

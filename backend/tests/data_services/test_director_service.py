from app.data_services.director_service import DirectorService
from app.exceptions import NotFoundError
from app.schemas.director import DirectorFilters


def test_list_directors_filters_by_search(db_session, sample_catalog):
    del sample_catalog
    service = DirectorService()

    items, pagination = service.list(
        db_session,
        DirectorFilters(search="Nolan", page=1, page_size=10),
    )

    assert [item.name for item in items] == ["Christopher Nolan"]
    assert pagination.total == 1


def test_get_director_movies_returns_movies(db_session, sample_catalog):
    del sample_catalog
    service = DirectorService()

    items, pagination = service.get_director_movies(db_session, director_id=1, page=1, page_size=10)

    assert [item.title for item in items] == ["Oppenheimer"]
    assert pagination.total == 1


def test_get_director_movies_raises_for_missing_director(db_session):
    service = DirectorService()

    try:
        service.get_director_movies(db_session, director_id=999, page=1, page_size=10)
    except NotFoundError as exc:
        assert exc.code == "not_found"
    else:
        raise AssertionError("Expected NotFoundError")

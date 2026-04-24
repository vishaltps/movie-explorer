from app.data_services.review_service import ReviewService
from app.exceptions import NotFoundError


def test_list_for_movie_returns_reviews(db_session, sample_catalog):
    del sample_catalog
    service = ReviewService()

    items, pagination = service.list_for_movie(db_session, movie_id=1, page=1, page_size=10)

    assert [item.author_name for item in items] == ["alice"]
    assert pagination.total == 1


def test_list_for_movie_raises_for_missing_movie(db_session):
    service = ReviewService()

    try:
        service.list_for_movie(db_session, movie_id=999, page=1, page_size=10)
    except NotFoundError as exc:
        assert exc.code == "not_found"
    else:
        raise AssertionError("Expected NotFoundError")

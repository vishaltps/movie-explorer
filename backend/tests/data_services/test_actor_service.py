from app.data_services.actor_service import ActorService
from app.exceptions import NotFoundError
from app.schemas.actor import ActorFilters


def test_list_actors_can_filter_by_movie_and_genre(db_session, sample_catalog):
    del sample_catalog
    service = ActorService()

    movie_items, _ = service.list(db_session, ActorFilters(movie_id=1, page=1, page_size=10))
    genre_items, _ = service.list(db_session, ActorFilters(genre_id=3, page=1, page_size=10))

    assert {item.name for item in movie_items} == {"Cillian Murphy", "Emily Blunt"}
    assert [item.name for item in genre_items] == ["Amy Adams"]


def test_list_actors_can_search(db_session, sample_catalog):
    del sample_catalog
    service = ActorService()

    items, pagination = service.list(db_session, ActorFilters(search="Amy", page=1, page_size=10))

    assert [item.name for item in items] == ["Amy Adams"]
    assert pagination.total == 1


def test_get_actor_movies_returns_movies(db_session, sample_catalog):
    del sample_catalog
    service = ActorService()

    items, pagination = service.get_actor_movies(db_session, actor_id=1, page=1, page_size=10)

    assert [item.title for item in items] == ["Oppenheimer"]
    assert pagination.total == 1


def test_get_actor_movies_raises_for_missing_actor(db_session):
    service = ActorService()

    try:
        service.get_actor_movies(db_session, actor_id=999, page=1, page_size=10)
    except NotFoundError as exc:
        assert exc.code == "not_found"
    else:
        raise AssertionError("Expected NotFoundError")

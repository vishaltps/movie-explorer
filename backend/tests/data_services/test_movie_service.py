from app.data_services.movie_service import MovieService
from app.exceptions import NotFoundError
from app.schemas.movie import MovieFilters


def test_list_movies_supports_filters_and_sort(db_session, sample_catalog):
    del sample_catalog
    service = MovieService()

    filtered, filtered_pagination = service.list(
        db_session,
        MovieFilters(
            genre_id=3,
            actor_id=3,
            director_id=2,
            search="Arrival",
            page=1,
            page_size=10,
        ),
    )
    sorted_items, sorted_pagination = service.list(
        db_session,
        MovieFilters(sort="-release_year", page=1, page_size=10),
    )

    assert [movie.title for movie in filtered] == ["Arrival"]
    assert filtered_pagination.total == 1
    assert [movie.title for movie in sorted_items] == ["Oppenheimer", "Arrival"]
    assert sorted_pagination.total == 2


def test_get_detail_loads_relationships(db_session, sample_catalog):
    del sample_catalog
    service = MovieService()

    movie = service.get_detail(db_session, 1)

    assert movie.title == "Oppenheimer"
    assert movie.director is not None
    assert movie.director.name == "Christopher Nolan"
    assert [genre.name for genre in movie.genres] == ["Drama", "History"]
    assert {actor.name for actor in movie.actors} == {"Cillian Murphy", "Emily Blunt"}
    assert movie.reviews[0].author_name == "alice"


def test_get_detail_raises_for_missing_movie(db_session):
    service = MovieService()

    try:
        service.get_detail(db_session, 999)
    except NotFoundError as exc:
        assert exc.code == "not_found"
    else:
        raise AssertionError("Expected NotFoundError")

from app.data_services.genre_service import GenreService


def test_list_all_returns_genres_sorted(db_session, sample_catalog):
    del sample_catalog
    service = GenreService()

    genres = service.list_all(db_session)

    assert [genre.name for genre in genres] == ["Drama", "History", "Sci-Fi"]

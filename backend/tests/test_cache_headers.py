def test_genres_have_long_cache(client):
    response = client.get("/api/v1/genres")

    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "public, max-age=600"


def test_movies_have_short_cache(client):
    response = client.get("/api/v1/movies")

    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "public, max-age=60"


def test_health_has_short_cache(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "public, max-age=60"


def test_error_responses_have_no_cache_header(client):
    response = client.get("/api/v1/movies/999")

    assert response.status_code == 404
    assert "Cache-Control" not in response.headers

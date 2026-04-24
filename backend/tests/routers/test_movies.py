def test_list_movies(client):
    response = client.get("/api/v1/movies")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert [item["title"] for item in payload["data"]] == ["Arrival", "Oppenheimer"]
    assert payload["meta"]["pagination"]["total"] == 2


def test_get_movie(client):
    response = client.get("/api/v1/movies/1")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["director"]["name"] == "Christopher Nolan"
    assert payload["data"]["reviews"][0]["author_name"] == "alice"

def test_list_reviews(client):
    response = client.get("/api/v1/movies/1/reviews")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"][0]["author_name"] == "alice"
    assert payload["meta"]["pagination"]["total"] == 1

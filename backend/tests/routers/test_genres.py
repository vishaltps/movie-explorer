def test_list_genres(client):
    response = client.get("/api/v1/genres")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert [item["name"] for item in payload["data"]] == ["Drama", "History", "Sci-Fi"]

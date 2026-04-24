def test_list_directors(client):
    response = client.get("/api/v1/directors")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"][0]["name"] == "Christopher Nolan"
    assert payload["meta"]["pagination"]["total"] == 2

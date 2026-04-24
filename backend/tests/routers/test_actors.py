def test_list_actors(client):
    response = client.get("/api/v1/actors")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"][0]["name"] == "Amy Adams"
    assert payload["meta"]["pagination"]["total"] == 3

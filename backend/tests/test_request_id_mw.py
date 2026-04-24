def test_request_id_header_echo(client):
    response = client.get("/api/v1/health", headers={"X-Request-ID": "abc-123"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "abc-123"

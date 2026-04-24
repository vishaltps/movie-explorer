from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.main import app


def test_not_found_returns_enveloped_error(client):
    response = client.get("/api/v1/genres/999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_generic_error_returns_internal_error(client):
    router = APIRouter()

    @router.get("/boom")
    def boom():
        raise RuntimeError("boom")

    app.include_router(router)
    try:
        with TestClient(app, raise_server_exceptions=False) as local_client:
            response = local_client.get("/boom")
        assert response.status_code == 500
        assert response.json()["error"]["code"] == "internal_error"
    finally:
        app.router.routes.pop()

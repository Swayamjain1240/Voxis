from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(app, base_url="http://localhost")


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["name"] == "VOXIS"
    assert data["status"] == "running"
    assert data["phase"] == 1


def test_health():
    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["status"] == "ok"
    assert data["components"]["api"] == "ready"


def test_liveness():
    response = client.get(
        "/api/v1/health/live"
    )

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "alive"

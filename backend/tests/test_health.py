from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "VOXIS"
    assert data["status"] == "running"
    assert data["phase"] == 1


def test_health():
    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["components"]["api"] == "ready"


def test_liveness():
    response = client.get(
        "/api/v1/health/live"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "alive"

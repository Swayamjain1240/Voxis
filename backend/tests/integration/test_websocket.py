from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(app)


def test_websocket_connection():
    with client.websocket_connect(
        "/ws"
    ) as websocket:
        event = websocket.receive_json()

        assert event["type"] == (
            "system.ready"
        )
        assert (
            event["data"]["mode"]
            == "mode-1"
        )

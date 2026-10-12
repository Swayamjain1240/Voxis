import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.main import create_app


@pytest.mark.parametrize("origin", [None, "http://localhost:5173", "https://untrusted.example"])
def test_websocket_cannot_connect_or_broadcast(origin):
    headers = {} if origin is None else {"origin": origin}
    with TestClient(create_app(), base_url="http://localhost") as client:
        with pytest.raises(WebSocketDisconnect) as error:
            with client.websocket_connect("/ws", headers=headers):
                pytest.fail("Mode 1 must not accept WebSocket connections")
    assert error.value.code == 1008

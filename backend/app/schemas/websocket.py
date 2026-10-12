from typing import Literal

from app.schemas.common import ContractModel, Version


class WebSocketTransportStatus(ContractModel):
    """The only WebSocket state exposed by the Mode 1 runtime."""

    schema_version: Version = "1.0.0"
    transport: Literal["websocket"] = "websocket"
    status: Literal["disabled"] = "disabled"
    mode: Literal["mode-1"] = "mode-1"

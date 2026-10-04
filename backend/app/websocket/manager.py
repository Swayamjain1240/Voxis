from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: list[
            WebSocket
        ] = []

    async def connect(
        self,
        websocket: WebSocket,
    ):
        await websocket.accept()

        if websocket not in self.connections:
            self.connections.append(
                websocket
            )

    def disconnect(
        self,
        websocket: WebSocket,
    ):
        if websocket in self.connections:
            self.connections.remove(
                websocket
            )

    async def send_personal(
        self,
        websocket: WebSocket,
        message: dict,
    ):
        await websocket.send_json(
            message
        )

    async def broadcast(
        self,
        message: dict,
    ):
        dead_connections = []

        for websocket in list(
            self.connections
        ):
            try:
                await websocket.send_json(
                    message
                )
            except Exception:
                dead_connections.append(
                    websocket
                )

        for websocket in dead_connections:
            self.disconnect(
                websocket
            )


connection_manager = (
    ConnectionManager()
)

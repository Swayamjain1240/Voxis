from app.websocket.events import (
    build_event,
)
from app.websocket.manager import (
    connection_manager,
)


async def handle_client_event(
    payload: dict,
):
    event_type = payload.get(
        "type",
        "conversation.message",
    )

    event_data = payload.get(
        "data",
        {},
    )

    event = build_event(
        event_type,
        event_data,
    )

    await connection_manager.broadcast(
        event
    )

    return event

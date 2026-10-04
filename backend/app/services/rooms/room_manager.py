from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Room:
    room_id: str
    participants: list[str]


class RoomManager:
    """
    Mode 2 infrastructure boundary.

    Mode 1 remains the current hackathon priority.
    """

    enabled = False

    def __init__(self):
        self.rooms: dict[str, Room] = {}

    def status(self):
        return {
            "enabled": self.enabled,
            "room_count": len(
                self.rooms
            ),
            "mode": "mode-1",
        }

    def create_room(self):
        if not self.enabled:
            raise RuntimeError(
                "Mode 2 rooms are disabled."
            )

        room_id = uuid4().hex[:8]

        room = Room(
            room_id=room_id,
            participants=[],
        )

        self.rooms[room_id] = room

        return {
            "room_id": room_id,
            "participants": [],
        }

    def join_room(self):
        if not self.enabled:
            raise RuntimeError(
                "Mode 2 rooms are disabled."
            )

        raise NotImplementedError


room_manager = RoomManager()

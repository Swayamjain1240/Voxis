import time

from pydantic import BaseModel, Field


class WebSocketEvent(BaseModel):
    type: str
    data: dict = Field(
        default_factory=dict
    )
    timestamp: int = Field(
        default_factory=lambda:
            int(time.time() * 1000)
    )

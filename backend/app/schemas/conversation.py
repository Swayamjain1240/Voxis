import time

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    id: str
    source: str
    text: str
    glosses: list[str] = Field(
        default_factory=list
    )
    timestamp: int = Field(
        default_factory=lambda:
            int(time.time() * 1000)
    )


class ConversationTurn(
    ConversationMessage
):
    pass

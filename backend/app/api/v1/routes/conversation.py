import time

from fastapi import APIRouter

from app.schemas.conversation import (
    ConversationMessage,
    ConversationTurn,
)
from app.services.language.gloss_to_text import (
    gloss_to_text,
)
from app.services.language.text_to_gloss import (
    text_to_gloss,
)


router = APIRouter()


@router.post(
    "/message",
    response_model=ConversationTurn,
)
async def message(
    payload: ConversationMessage,
):
    glosses = payload.glosses

    if (
        payload.source == "speech"
        and not glosses
        and payload.text
    ):
        glosses = text_to_gloss(
            payload.text
        )

    return ConversationTurn(
        id=payload.id,
        source=payload.source,
        text=payload.text,
        glosses=glosses,
        timestamp=payload.timestamp
        or int(time.time() * 1000),
    )


@router.post("/text-to-gloss")
async def convert_text_to_gloss(
    text: str,
):
    glosses = text_to_gloss(text)

    return {
        "text": text,
        "glosses": glosses,
        "source": "deterministic",
        "phase": 3,
    }


@router.post("/gloss-to-text")
async def convert_gloss_to_text(
    glosses: list[str],
):
    text = gloss_to_text(glosses)

    return {
        "glosses": glosses,
        "text": text,
        "source": "deterministic",
        "phase": 5,
    }

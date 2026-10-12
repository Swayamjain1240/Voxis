from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request

from app.schemas.common import Context
from app.schemas.conversation import (
    ConversationInput, ConversationTurn, GlossToTextRequest, TextToGlossRequest,
)
from app.schemas.response import ApiResponse, success
from app.services.language.gloss_to_text import gloss_to_text
from app.services.language.text_to_gloss import text_to_gloss


router = APIRouter()


@router.post("/message", response_model=ApiResponse[ConversationTurn])
async def message(request: Request, payload: ConversationInput):
    data = payload.model_dump()
    if payload.source == "speech" and not payload.glosses:
        data["glosses"] = text_to_gloss(payload.text, context=payload.context)
    # Stateless normalization: no shared transcript or persistence side effect.
    return success(request, ConversationTurn(**data))


@router.post("/text-to-gloss", response_model=ApiResponse[dict])
async def convert_text_to_gloss(
    request: Request,
    payload: TextToGlossRequest | None = None,
    text: Annotated[str | None, Query(min_length=1, max_length=4000)] = None,
    context: Annotated[Context | None, Query()] = None,
):
    if payload is not None and (text is not None or context is not None):
        raise HTTPException(400, "Supply either a JSON body or legacy query input.")
    if payload is None:
        if text is None:
            raise HTTPException(422, "A text input is required.")
        # Feed the compatibility input through the same validated request model.
        from fastapi.exceptions import RequestValidationError
        from pydantic import ValidationError
        try:
            payload = TextToGlossRequest(text=text, context=context)
        except ValidationError as error:
            raise RequestValidationError(error.errors()) from error
    return success(request, {
        "text": payload.text,
        "glosses": text_to_gloss(payload.text, context=payload.context),
        "context": payload.context,
        "source": "deterministic",
        "vocabulary_version": "1.0.0",
    })


@router.post("/gloss-to-text", response_model=ApiResponse[dict])
async def convert_gloss_to_text(request: Request, payload: GlossToTextRequest):
    return success(request, {
        "glosses": payload.glosses,
        "text": gloss_to_text(payload.glosses),
        "context": payload.context,
        "source": "deterministic",
        "vocabulary_version": "1.0.0",
    })

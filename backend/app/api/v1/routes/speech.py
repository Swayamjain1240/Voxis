from fastapi import APIRouter, File, UploadFile

from app.core.exceptions import FeatureNotEnabledError
from app.schemas.speech import (
    AudioUploadResponse,
    TranscriptionResponse,
)
from app.services.speech.audio_processor import (
    validate_audio_upload,
)
from app.services.speech.whisper_service import WhisperService


router = APIRouter()

whisper_service = WhisperService()


@router.get("/capabilities")
async def capabilities():
    return {
        "microphone_capture": True,
        "audio_upload": True,
        "transcription": whisper_service.enabled,
        "language": "en",
        "phase": 1,
    }


@router.post(
    "/upload",
    response_model=AudioUploadResponse,
)
async def upload_audio(
    audio: UploadFile = File(...),
):
    metadata = await validate_audio_upload(audio)

    return AudioUploadResponse(
        filename=metadata.filename,
        content_type=metadata.content_type,
        size_bytes=metadata.size_bytes,
        duration_ms=None,
        accepted=True,
    )


@router.post(
    "/transcribe",
    response_model=TranscriptionResponse,
)
async def transcribe(
    audio: UploadFile = File(...),
):
    metadata = await validate_audio_upload(audio)

    try:
        return await whisper_service.transcribe(
            audio_bytes=metadata.content,
            filename=metadata.filename,
            content_type=metadata.content_type,
        )

    except FeatureNotEnabledError:
        raise

from fastapi import APIRouter, File, Request, UploadFile

from app.core.exceptions import FeatureNotEnabledError
from app.schemas.speech import (
    AudioUploadResponse,
    TranscriptionResponse,
)
from app.services.speech.audio_processor import (
    validate_audio_upload,
)
from app.services.speech.whisper_service import WhisperService
from app.schemas.response import ApiResponse, success


router = APIRouter()

whisper_service = WhisperService()


@router.get("/capabilities")
async def capabilities(request: Request):
    status = whisper_service.status()
    return success(request, {
        "microphone_capture": True,
        "audio_upload": True,
        "transcription": status["available"],
        "transcription_status": status["status"],
        "language": "en",
        "phase": 1,
    })


@router.post(
    "/upload",
    response_model=ApiResponse[AudioUploadResponse],
)
async def upload_audio(
    request: Request,
    audio: UploadFile = File(...),
):
    metadata = await validate_audio_upload(
        audio,
        max_audio_upload_mb=request.app.state.settings.max_audio_upload_mb,
    )

    return success(request, AudioUploadResponse(
        filename=metadata.filename,
        content_type=metadata.content_type,
        size_bytes=metadata.size_bytes,
        duration_ms=None,
        accepted=True,
    ))


@router.post(
    "/transcribe",
    response_model=ApiResponse[TranscriptionResponse],
)
async def transcribe(
    request: Request,
    audio: UploadFile = File(...),
):
    metadata = await validate_audio_upload(
        audio,
        max_audio_upload_mb=request.app.state.settings.max_audio_upload_mb,
    )

    try:
        result = await whisper_service.transcribe(
            audio_bytes=metadata.content,
            filename=metadata.filename,
            content_type=metadata.content_type,
        )
        return success(request, result)

    except FeatureNotEnabledError:
        raise

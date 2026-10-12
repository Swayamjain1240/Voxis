from fastapi import APIRouter

from app.core.config import settings
from app.services.sign_recognition.inference import SignInferenceService
from app.services.speech.whisper_service import WhisperService
from app.services.tts.tts_service import TTSService


router = APIRouter()

whisper_service = WhisperService()
sign_service = SignInferenceService()
tts_service = TTSService()


def _llm_status() -> str:
    return "unavailable" if settings.llm_enabled else "deterministic-fallback"


@router.get("")
async def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
        "phase": 1,
        "components": {
            "api": "ready",
            "speech_capture": "frontend",
            "audio_upload": "ready",
            "whisper": whisper_service.status()["status"],
            "text_to_gloss": _llm_status(),
            "sign_model": sign_service.status()["status"],
            "tts": tts_service.status()["status"],
            "websocket": "ready",
        },
    }


@router.get("/live")
async def liveness():
    return {"status": "alive"}


@router.get("/ready")
async def readiness():
    return {
        "status": "ready",
        "phase": 1,
    }

from fastapi import APIRouter

from app.core.config import settings


router = APIRouter()


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
            "whisper": (
                "enabled"
                if settings.whisper_enabled
                else "phase-2-disabled"
            ),
            "text_to_gloss": (
                "enabled"
                if settings.llm_enabled
                else "deterministic-fallback"
            ),
            "sign_model": (
                "enabled"
                if settings.sign_model_enabled
                else "phase-3-disabled"
            ),
            "tts": (
                "enabled"
                if settings.tts_enabled
                else "phase-5-disabled"
            ),
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

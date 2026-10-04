from app.core.config import settings
from app.core.exceptions import (
    FeatureNotEnabledError,
)


class TTSService:
    def __init__(self):
        self.enabled = (
            settings.tts_enabled
        )

    async def synthesize(
        self,
        text: str,
    ):
        if not self.enabled:
            raise FeatureNotEnabledError(
                "Text-to-Speech",
                "Phase 5",
            )

        return {
            "text": text,
            "audio_url": None,
            "provider": None,
        }

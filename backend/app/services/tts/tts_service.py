from app.core.config import settings
from app.core.exceptions import (
    FeatureNotEnabledError,
    FeatureUnavailableError,
)


class TTSService:
    def __init__(self, enabled: bool | None = None):
        self.enabled = (
            settings.tts_enabled
            if enabled is None
            else enabled
        )

    @property
    def implemented(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        return self.enabled and self.implemented

    def status(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "implemented": self.implemented,
            "available": self.available,
            "status": "disabled" if not self.enabled else "unavailable",
            "runtime": "not-implemented",
        }

    async def synthesize(
        self,
        text: str,
    ):
        if not self.enabled:
            raise FeatureNotEnabledError(
                "Text-to-Speech",
                "Phase 5",
            )

        raise FeatureUnavailableError(
            "Text-to-Speech",
            "TTS_UNAVAILABLE",
        )

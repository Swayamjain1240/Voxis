from app.core.config import settings
from app.core.exceptions import (
    FeatureNotEnabledError,
    FeatureUnavailableError,
)


class WhisperService:
    """
    Whisper service boundary.

    Phase 1:
        Capture/upload only.

    Phase 2:
        Plug local Whisper/faster-whisper behind this interface.
    """

    def __init__(self, enabled: bool | None = None):
        self.enabled = (
            settings.whisper_enabled
            if enabled is None
            else enabled
        )
        self.model = None

    @property
    def implemented(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        return self.enabled and self.implemented and self.model is not None

    def status(self) -> dict[str, object]:
        if not self.enabled:
            state = "disabled"
        elif not self.implemented:
            state = "unavailable"
        else:
            state = "available" if self.available else "unavailable"
        return {
            "enabled": self.enabled,
            "implemented": self.implemented,
            "available": self.available,
            "status": state,
            "runtime": "not-implemented" if not self.implemented else "pending",
        }

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ):

        if not self.enabled:
            raise FeatureNotEnabledError(
                "Whisper transcription",
                "Phase 2",
            )

        raise FeatureUnavailableError(
            "Whisper transcription",
            "WHISPER_UNAVAILABLE",
        )

    def load(self):
        if not self.enabled:
            return

        raise FeatureUnavailableError(
            "Whisper transcription",
            "WHISPER_UNAVAILABLE",
        )

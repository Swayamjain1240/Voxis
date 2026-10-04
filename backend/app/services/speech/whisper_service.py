import time

from app.core.config import settings
from app.core.exceptions import (
    FeatureNotEnabledError,
)
from app.schemas.speech import (
    TranscriptionResponse,
)


class WhisperService:
    """
    Whisper service boundary.

    Phase 1:
        Capture/upload only.

    Phase 2:
        Plug local Whisper/faster-whisper behind this interface.
    """

    def __init__(self):
        self.enabled = (
            settings.whisper_enabled
        )
        self.model = None

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> TranscriptionResponse:

        if not self.enabled:
            raise FeatureNotEnabledError(
                "Whisper transcription",
                "Phase 2",
            )

        # Keep the interface stable.
        #
        # Example future implementation:
        #
        # segments, info = self.model.transcribe(...)
        #
        # The frontend should not need to change.

        return TranscriptionResponse(
            text="",
            language="en",
            confidence=None,
            source="whisper",
            timestamp=int(
                time.time() * 1000
            ),
        )

    def load(self):
        if not self.enabled:
            return

        # Model initialization belongs here.
        # Not loaded during Phase 1.

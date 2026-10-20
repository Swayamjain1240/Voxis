from __future__ import annotations

import asyncio
import math
from pathlib import Path
import tempfile
from typing import Any

from app.core.config import settings
from app.core.exceptions import (
    FeatureNotEnabledError,
    FeatureUnavailableError,
    InvalidAudioError,
)
from app.schemas.speech import TranscriptionResponse


class WhisperService:
    """
    Whisper service boundary.

    Local faster-whisper adapter. The optional dependency and model are loaded
    only when transcription is explicitly enabled and requested.
    """

    def __init__(self, enabled: bool | None = None, model: Any | None = None):
        self.enabled = (
            settings.whisper_enabled
            if enabled is None
            else enabled
        )
        self.model = model
        self._load_error = ""

    @property
    def implemented(self) -> bool:
        return True

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
            "runtime": "faster-whisper" if self.model is not None else "not-loaded",
            "model_loaded": self.model is not None,
        }

    def load(self) -> bool:
        if not self.enabled:
            return False
        if self.model is not None:
            return True

        try:
            from faster_whisper import WhisperModel
        except ImportError as error:
            self._load_error = "Install the optional faster-whisper runtime."
            raise FeatureUnavailableError(
                "Whisper transcription",
                "WHISPER_UNAVAILABLE",
                self._load_error,
            ) from error

        model_source = settings.whisper_model_path or settings.whisper_model_size
        try:
            self.model = WhisperModel(
                model_source,
                device=settings.whisper_device,
                compute_type=settings.whisper_compute_type,
            )
        except Exception as error:
            self._load_error = "The configured local Whisper model could not be loaded."
            raise FeatureUnavailableError(
                "Whisper transcription",
                "WHISPER_UNAVAILABLE",
                self._load_error,
            ) from error
        return True

    @staticmethod
    def _segment_text(segment: Any) -> str:
        value = segment.get("text", "") if isinstance(segment, dict) else getattr(segment, "text", "")
        return " ".join(str(value).split())

    @staticmethod
    def _confidence(info: Any, segments: list[Any]) -> float | None:
        language_probability = getattr(info, "language_probability", None)
        if isinstance(language_probability, (int, float)) and math.isfinite(language_probability):
            return max(0.0, min(1.0, float(language_probability)))
        log_probs = [
            float(getattr(segment, "avg_logprob"))
            for segment in segments
            if isinstance(getattr(segment, "avg_logprob", None), (int, float))
            and math.isfinite(float(getattr(segment, "avg_logprob")))
        ]
        if not log_probs:
            return None
        return max(0.0, min(1.0, math.exp(sum(log_probs) / len(log_probs))))

    def _transcribe_sync(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> TranscriptionResponse:
        self.load()
        suffix = Path(filename).suffix or ".audio"
        temporary_path: str | None = None
        try:
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as handle:
                handle.write(audio_bytes)
                temporary_path = handle.name
            try:
                result = self.model.transcribe(
                    temporary_path,
                    language="en",
                    vad_filter=True,
                    beam_size=5,
                )
                if isinstance(result, tuple):
                    raw_segments, info = result
                else:
                    raw_segments, info = result, None
                segments = list(raw_segments)
            except Exception as error:
                raise FeatureUnavailableError(
                    "Whisper transcription",
                    "WHISPER_RUNTIME_ERROR",
                    "The local Whisper runtime could not process this audio.",
                ) from error
        finally:
            if temporary_path:
                Path(temporary_path).unlink(missing_ok=True)

        transcript = " ".join(
            text for text in (self._segment_text(segment) for segment in segments) if text
        ).strip()
        if not transcript:
            raise InvalidAudioError("No speech was detected in the audio.")

        return TranscriptionResponse(
            transcript=transcript[:4000],
            language="en",
            confidence=self._confidence(info, segments),
            source="microphone",
        )

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

        return await asyncio.to_thread(
            self._transcribe_sync,
            audio_bytes,
            filename,
            content_type,
        )

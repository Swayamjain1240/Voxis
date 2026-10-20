from typing import Literal

from pydantic import Field

from app.schemas.common import ContractModel, GlossList, Text, Timestamp, Version, utc_now


class AudioUploadResponse(ContractModel):
    filename: str
    content_type: str
    size_bytes: int = Field(
        ge=0
    )
    duration_ms: int | None = None
    quality_status: Literal["ok", "too_short", "silent", "unknown"] = "unknown"
    quality_warning: str | None = None
    accepted: bool


class TranscriptionResponse(ContractModel):
    type: Literal["speech_result"] = "speech_result"
    schema_version: Version = "1.0.0"
    vocabulary_version: Version = "1.0.0"
    transcript: Text
    language: Literal["en"] = "en"
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
    glosses: GlossList = Field(default_factory=list)
    source: Literal["microphone", "audio_file", "api"] = "microphone"
    timestamp: Timestamp = Field(default_factory=utc_now)

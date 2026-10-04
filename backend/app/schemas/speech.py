from pydantic import BaseModel, Field


class AudioUploadResponse(BaseModel):
    filename: str
    content_type: str
    size_bytes: int = Field(
        ge=0
    )
    duration_ms: int | None = None
    accepted: bool


class TranscriptionResponse(BaseModel):
    text: str
    language: str
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
    source: str = "whisper"
    timestamp: int

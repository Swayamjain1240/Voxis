from dataclasses import dataclass

from fastapi import (
    HTTPException,
    UploadFile,
)

from app.core.config import settings


@dataclass
class AudioMetadata:
    filename: str
    content_type: str
    size_bytes: int
    content: bytes


SUPPORTED_AUDIO_PREFIX = "audio/"


async def validate_audio_upload(
    audio: UploadFile,
) -> AudioMetadata:
    filename = (
        audio.filename
        or "speech-audio"
    )

    content_type = (
        audio.content_type
        or "application/octet-stream"
    ).lower()

    if not content_type.startswith(
        SUPPORTED_AUDIO_PREFIX
    ):
        raise HTTPException(
            status_code=415,
            detail=(
                "Unsupported content type. "
                "Only audio uploads are accepted."
            ),
        )

    content = await audio.read()

    max_bytes = (
        settings.max_audio_upload_mb
        * 1024
        * 1024
    )

    if len(content) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=(
                "Audio exceeds the configured "
                f"{settings.max_audio_upload_mb} MB limit."
            ),
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Audio file is empty.",
        )

    return AudioMetadata(
        filename=filename,
        content_type=content_type,
        size_bytes=len(content),
        content=content,
    )

from dataclasses import dataclass
from typing import BinaryIO

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import (
    InvalidAudioError,
    PayloadTooLargeError,
    UnsupportedMediaTypeError,
)


@dataclass
class AudioMetadata:
    filename: str
    content_type: str
    size_bytes: int
    content: bytes


READ_CHUNK_BYTES = 64 * 1024
SUPPORTED_AUDIO_TYPES = frozenset({
    "audio/aac",
    "audio/mp4",
    "audio/mpeg",
    "audio/ogg",
    "audio/wav",
    "audio/webm",
    "audio/x-wav",
})


def _safe_filename(filename: str | None) -> str:
    value = (filename or "speech-audio").strip()
    if not value or len(value) > 255 or any(
        ord(char) < 32 or ord(char) == 127 or char in {"/", "\\"}
        for char in value
    ):
        raise InvalidAudioError("Audio filename is invalid.")
    return value


def _content_type(value: str | None) -> str:
    return (value or "").split(";", 1)[0].strip().lower()


def _has_audio_signature(content_type: str, content: bytes) -> bool:
    if content_type == "audio/webm":
        return content.startswith(b"\x1a\x45\xdf\xa3")
    if content_type == "audio/ogg":
        return content.startswith(b"OggS")
    if content_type in {"audio/wav", "audio/x-wav"}:
        return len(content) >= 12 and content[:4] in {b"RIFF", b"RF64"} and content[8:12] == b"WAVE"
    if content_type == "audio/mp4":
        return len(content) >= 12 and content[4:8] == b"ftyp"
    if content_type == "audio/mpeg":
        return content.startswith(b"ID3") or (
            len(content) >= 2 and content[0] == 0xFF and content[1] & 0xE0 == 0xE0
        )
    if content_type == "audio/aac":
        return len(content) >= 2 and content[0] == 0xFF and content[1] & 0xF6 == 0xF0
    return False


async def _read_bounded(file: BinaryIO, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while total <= max_bytes:
        chunk = await file.read(min(READ_CHUNK_BYTES, max_bytes - total + 1))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise PayloadTooLargeError("Audio exceeds the configured upload limit.")
    return b"".join(chunks)


async def validate_audio_upload(
    audio: UploadFile,
    *,
    max_audio_upload_mb: int | None = None,
) -> AudioMetadata:
    filename = _safe_filename(audio.filename)
    content_type = _content_type(audio.content_type)
    if content_type not in SUPPORTED_AUDIO_TYPES:
        raise UnsupportedMediaTypeError(
            "Unsupported audio format. Use WebM, Ogg, WAV, MP4, AAC, or MPEG audio.",
        )

    max_mb = settings.max_audio_upload_mb if max_audio_upload_mb is None else max_audio_upload_mb
    if not 1 <= max_mb <= 50:
        raise PayloadTooLargeError("Audio upload limit is outside the supported range.")
    max_bytes = max_mb * 1024 * 1024
    content = await _read_bounded(audio, max_bytes)

    if not content:
        raise InvalidAudioError("Audio file is empty.")
    if not _has_audio_signature(content_type, content):
        raise InvalidAudioError("Audio content does not match the declared format.")

    return AudioMetadata(
        filename=filename,
        content_type=content_type,
        size_bytes=len(content),
        content=content,
    )

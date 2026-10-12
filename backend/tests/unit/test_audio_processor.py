from io import BytesIO
import wave

import pytest
from fastapi import UploadFile

from app.core.exceptions import InvalidAudioError, PayloadTooLargeError, UnsupportedMediaTypeError
from app.services.speech.audio_processor import validate_audio_upload


def wav_fixture(frame_count: int = 1) -> bytes:
    output = BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(8000)
        wav.writeframes(b"\x00\x00" * frame_count)
    return output.getvalue()


def upload(content: bytes, *, content_type: str = "audio/wav", filename: str = "sample.wav"):
    return UploadFile(filename=filename, file=BytesIO(content), headers={"content-type": content_type})


@pytest.mark.anyio
async def test_valid_audio_is_read_in_bounded_chunks():
    result = await validate_audio_upload(upload(wav_fixture()))
    assert result.content_type == "audio/wav"
    assert result.size_bytes == len(result.content)
    assert result.content.startswith(b"RIFF")


@pytest.mark.anyio
async def test_empty_audio_is_rejected():
    with pytest.raises(InvalidAudioError, match="empty"):
        await validate_audio_upload(upload(b""))


@pytest.mark.anyio
async def test_mime_type_alone_does_not_make_text_audio():
    with pytest.raises(InvalidAudioError, match="match"):
        await validate_audio_upload(upload(b"fake-audio-content"))


@pytest.mark.anyio
async def test_unsupported_type_is_rejected_before_reading():
    with pytest.raises(UnsupportedMediaTypeError):
        await validate_audio_upload(upload(wav_fixture(), content_type="application/octet-stream"))


@pytest.mark.anyio
async def test_filename_paths_and_controls_are_rejected():
    with pytest.raises(InvalidAudioError, match="filename"):
        await validate_audio_upload(upload(wav_fixture(), filename="..\\private.wav"))


@pytest.mark.anyio
async def test_upload_size_is_checked_before_unbounded_buffering():
    with pytest.raises(PayloadTooLargeError):
        await validate_audio_upload(upload(wav_fixture(600_000)), max_audio_upload_mb=1)

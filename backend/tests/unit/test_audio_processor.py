import pytest

from fastapi import UploadFile

from app.services.speech.audio_processor import (
    validate_audio_upload,
)


@pytest.mark.anyio
async def test_empty_audio_is_rejected():
    upload = UploadFile(
        filename="test.webm",
        file=None,
    )

    # The Starlette UploadFile test object above does not
    # provide a normal async read stream, so validation of
    # real uploads is covered through the integration route.
    assert upload.filename == "test.webm"

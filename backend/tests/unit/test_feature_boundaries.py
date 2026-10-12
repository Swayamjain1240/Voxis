import asyncio

import pytest

from app.core.exceptions import (
    FeatureNotEnabledError,
    FeatureUnavailableError,
)
from app.services.sign_recognition.inference import SignInferenceService
from app.services.speech.whisper_service import WhisperService
from app.services.tts.tts_service import TTSService


def test_disabled_services_report_disabled_and_raise():
    whisper = WhisperService(enabled=False)
    sign = SignInferenceService(enabled=False)
    tts = TTSService(enabled=False)

    assert whisper.status()["status"] == "disabled"
    assert sign.status()["status"] == "disabled"
    assert tts.status()["status"] == "disabled"

    with pytest.raises(FeatureNotEnabledError):
        asyncio.run(whisper.transcribe(b"audio", "test.webm", "audio/webm"))
    with pytest.raises(FeatureNotEnabledError):
        asyncio.run(sign.predict({"frames": []}))
    with pytest.raises(FeatureNotEnabledError):
        asyncio.run(tts.synthesize("hello"))


def test_enabled_placeholder_services_do_not_fabricate_success():
    whisper = WhisperService(enabled=True)
    sign = SignInferenceService(enabled=True)
    tts = TTSService(enabled=True)

    assert whisper.status()["status"] == "unavailable"
    assert sign.status()["status"] == "unavailable"
    assert tts.status()["status"] == "unavailable"

    with pytest.raises(FeatureUnavailableError):
        asyncio.run(whisper.transcribe(b"audio", "test.webm", "audio/webm"))
    with pytest.raises(FeatureUnavailableError):
        asyncio.run(sign.predict({"frames": []}))
    with pytest.raises(FeatureUnavailableError):
        asyncio.run(tts.synthesize("hello"))

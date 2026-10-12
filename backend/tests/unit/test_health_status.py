import asyncio
import importlib

from app.services.sign_recognition.inference import SignInferenceService
from app.services.speech.whisper_service import WhisperService
from app.services.tts.tts_service import TTSService


health_module = importlib.import_module("app.api.v1.routes.health")


def test_health_reports_disabled_optional_services_honestly():
    payload = health_module.component_health()
    components = payload["components"]

    assert components["whisper"] == "disabled"
    assert components["sign_model"] == "disabled"
    assert components["tts"] == "disabled"
    assert components["text_to_gloss"] == "deterministic-fallback"


def test_health_does_not_report_enabled_placeholders_as_ready(monkeypatch):
    monkeypatch.setattr(
        health_module,
        "whisper_service",
        WhisperService(enabled=True),
    )
    monkeypatch.setattr(
        health_module,
        "sign_service",
        SignInferenceService(enabled=True),
    )
    monkeypatch.setattr(
        health_module,
        "tts_service",
        TTSService(enabled=True),
    )

    payload = health_module.component_health()
    components = payload["components"]

    assert components["whisper"] == "unavailable"
    assert components["sign_model"] == "unavailable"
    assert components["tts"] == "unavailable"

from fastapi.testclient import TestClient
from io import BytesIO
import wave

from app.main import app
from app.api.v1.routes import speech, sign
from app.services.speech.whisper_service import WhisperService
from app.services.sign_recognition.inference import SignInferenceService


def wav_fixture():
    output = BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        audio.writeframes(b"\x00\x00")
    return output.getvalue()


def test_enabled_whisper_is_unavailable_over_http(monkeypatch):
    monkeypatch.setattr(speech, "whisper_service", WhisperService(enabled=True))
    with TestClient(app, base_url="http://localhost") as client:
        capabilities = client.get("/api/v1/speech/capabilities").json()["data"]
        assert capabilities["transcription"] is False
        assert capabilities["transcription_status"] == "unavailable"
        response = client.post(
            "/api/v1/speech/transcribe",
            files={"audio": ("sample.wav", wav_fixture(), "audio/wav")},
        )
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "WHISPER_UNAVAILABLE"
    assert "text" not in response.json()


def test_enabled_model_cannot_return_empty_success(monkeypatch):
    monkeypatch.setattr(sign, "sign_service", SignInferenceService(enabled=True))
    with TestClient(app, base_url="http://localhost") as client:
        response = client.post("/api/v1/sign/predict", json={"frames": [[0.0] * 300] * 60})
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SIGN_MODEL_UNAVAILABLE"


def test_validation_error_does_not_echo_user_input():
    with TestClient(app, base_url="http://localhost") as client:
        response = client.post(
            "/api/v1/sign/predict", json={"top_k": "private-user-input"}
        )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    assert "private-user-input" not in response.text


def test_not_found_has_error_envelope():
    with TestClient(app, base_url="http://localhost") as client:
        response = client.get("/not-a-route")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"

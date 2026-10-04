from io import BytesIO

from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(app)


def test_speech_capabilities():
    response = client.get(
        "/api/v1/speech/capabilities"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["microphone_capture"] is True
    assert data["audio_upload"] is True
    assert data["transcription"] is False


def test_audio_upload():
    audio = BytesIO(
        b"fake-audio-content"
    )

    response = client.post(
        "/api/v1/speech/upload",
        files={
            "audio": (
                "test.webm",
                audio,
                "audio/webm",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["accepted"] is True
    assert data["filename"] == "test.webm"
    assert data["size_bytes"] > 0


def test_empty_audio():
    response = client.post(
        "/api/v1/speech/upload",
        files={
            "audio": (
                "empty.webm",
                BytesIO(b""),
                "audio/webm",
            )
        },
    )

    assert response.status_code == 400

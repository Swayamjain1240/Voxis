from io import BytesIO
import wave

from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(app, base_url="http://localhost")


def wav_fixture():
    output = BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        audio.writeframes(b"\x00\x00")
    return output.getvalue()


def test_speech_capabilities():
    response = client.get(
        "/api/v1/speech/capabilities"
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["microphone_capture"] is True
    assert data["audio_upload"] is True
    assert data["transcription"] is False


def test_audio_upload():
    audio = BytesIO(wav_fixture())

    response = client.post(
        "/api/v1/speech/upload",
        files={
            "audio": (
                "test.wav",
                audio,
                "audio/wav",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["accepted"] is True
    assert data["filename"] == "test.wav"
    assert data["size_bytes"] > 0


def test_empty_audio():
    response = client.post(
        "/api/v1/speech/upload",
        files={
            "audio": (
                "empty.wav",
                BytesIO(b""),
                "audio/wav",
            )
        },
    )

    assert response.status_code == 400

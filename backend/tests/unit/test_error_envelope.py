import json

from app.core.exceptions import (
    FeatureUnavailableError,
    http_exception_handler,
)


def test_application_error_has_consistent_envelope():
    response = http_exception_handler(
        None,
        FeatureUnavailableError(
            "Whisper transcription",
            "WHISPER_UNAVAILABLE",
        ),
    )
    payload = json.loads(response.body)

    assert response.status_code == 503
    assert payload["success"] is False
    assert payload["error"]["code"] == "WHISPER_UNAVAILABLE"
    assert payload["detail"] == payload["error"]["message"]

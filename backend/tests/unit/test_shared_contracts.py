import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from app.schemas.conversation import ConversationMessage
from app.schemas.sign import SignPredictionResult
from app.schemas.speech import TranscriptionResponse
from app.schemas.websocket import WebSocketTransportStatus
from app.services.language.text_to_gloss import VOCABULARY


CONTRACTS = Path(__file__).resolve().parents[3] / "shared" / "contracts"


@pytest.mark.parametrize("filename,model", [
    ("conversation-message.schema.json", ConversationMessage(id="m-1", source="speech", text="help", glosses=["HELP"])),
    ("speech-result.schema.json", TranscriptionResponse(transcript="help", glosses=["HELP"])),
    ("sign-prediction.schema.json", SignPredictionResult(
        model_version="test-only", sequence_id="seq-1",
        prediction={"gloss": "UNKNOWN", "label": -1, "confidence": 0.1, "stable": False},
    )),
])
def test_serialized_runtime_messages_match_shared_schemas(filename, model):
    schema = json.loads((CONTRACTS / filename).read_text(encoding="utf-8-sig"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    payload = model.model_dump(mode="json")
    validator.validate(payload)
    payload["timestamp"] = 1000
    assert not validator.is_valid(payload)
    payload["timestamp"] = model.model_dump(mode="json")["timestamp"]
    payload["schema_version"] = "unknown"
    assert not validator.is_valid(payload)


def test_schema_vocabulary_cannot_silently_drift():
    for name in ("conversation-message", "speech-result"):
        schema = json.loads((CONTRACTS / f"{name}.schema.json").read_text(encoding="utf-8-sig"))
        assert set(schema["properties"]["glosses"]["items"]["enum"]) == VOCABULARY.glosses
        assert schema["properties"]["vocabulary_version"]["const"] == VOCABULARY.version


def test_disabled_websocket_status_matches_shared_contract():
    schema = json.loads((CONTRACTS / "websocket-events.schema.json").read_text(encoding="utf-8-sig"))
    payload = WebSocketTransportStatus().model_dump(mode="json")
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(payload)

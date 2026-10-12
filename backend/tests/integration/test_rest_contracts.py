import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator, FormatChecker

from app.main import app


def test_conversation_output_matches_shared_contract():
    with TestClient(app, base_url="http://localhost") as client:
        response = client.post("/api/v1/conversation/message", json={
            "id": "legacy-1", "source": "speech", "text": "doctor money",
            "context": "bank", "timestamp": 1000,
        })
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["glosses"] == ["MONEY"]
    assert body["meta"]["request_id"] == response.headers["x-request-id"]
    path = Path(__file__).resolve().parents[3] / "shared/contracts/conversation-message.schema.json"
    Draft202012Validator(json.loads(path.read_text()), format_checker=FormatChecker()).validate(body["data"])


@pytest.mark.parametrize("body", [
    {"glosses": ["NO_SUCH_SIGN"]}, {"glosses": ["DOCTOR"], "context": "bank"},
    {"glosses": []}, ["NO_SUCH_SIGN"],
])
def test_invalid_glosses_rejected_at_http_boundary(body):
    with TestClient(app, base_url="http://localhost") as client:
        response = client.post("/api/v1/conversation/gloss-to-text", json=body)
    assert response.status_code == 422
    assert response.json()["meta"]["request_id"] == response.headers["x-request-id"]


def test_json_and_legacy_gloss_requests_share_validation():
    with TestClient(app, base_url="http://localhost") as client:
        for body in ({"glosses": ["HELP"]}, ["HELP"]):
            result = client.post("/api/v1/conversation/gloss-to-text", json=body)
            assert result.status_code == 200
            assert result.json()["data"]["text"] == "I need help."


def test_json_text_contract_and_ambiguous_input():
    with TestClient(app, base_url="http://localhost") as client:
        result = client.post("/api/v1/conversation/text-to-gloss", json={"text": "help"})
        assert result.json()["data"]["glosses"] == ["HELP"]
        bad = client.post("/api/v1/conversation/text-to-gloss?text=help", json={"text": "pain"})
        assert bad.status_code == 400

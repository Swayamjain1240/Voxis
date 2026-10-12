import pytest
from pydantic import ValidationError

from app.schemas.conversation import ConversationInput, GlossToTextRequest
from app.schemas.sign import SignInferenceRequest, SignPrediction


@pytest.mark.parametrize("change", [
    {"source": "arbitrary"}, {"sender": "system"},
    {"glosses": ["NOT_SUPPORTED"]}, {"text": "x" * 4001},
    {"text": "hello\x00"}, {"extra": "ignored-before"},
    {"context": "bank", "glosses": ["DOCTOR"]},
])
def test_rejects_invalid_or_impersonated_conversation(change):
    with pytest.raises(ValidationError):
        ConversationInput.model_validate({"id": "test-1", "source": "speech", "text": "hello", **change})


def test_normalizes_legacy_identifier_and_millisecond_timestamp():
    result = ConversationInput(id="test-1", source="speech", text="help", timestamp=1000)
    data = result.model_dump(mode="json")
    assert data["message_id"] == "test-1"
    assert "id" not in data
    assert data["timestamp"] == "1970-01-01T00:00:01Z"
    assert data["modality"] == "speech"


@pytest.mark.parametrize("frames", [[], [[1.0]], [[0.0] * 299] * 60, [[0.0] * 300] * 61, [[float("nan")] * 300] * 60])
def test_rejects_wrong_landmark_shape_or_nonfinite_values(frames):
    with pytest.raises(ValidationError):
        SignInferenceRequest(frames=frames)


def test_accepts_canonical_raw_sequence():
    result = SignInferenceRequest(frames=[[0.0] * 300] * 60)
    assert result.sequence_length == 60


def test_unsupported_gloss_cannot_enter_language_conversion():
    with pytest.raises(ValidationError):
        GlossToTextRequest(glosses=["NOT_SUPPORTED"])


def test_unknown_prediction_cannot_claim_stability():
    with pytest.raises(ValidationError):
        SignPrediction(label=-1, gloss="UNKNOWN", confidence=0.9, stable=True)


def test_prediction_class_index_must_match_shared_label_map():
    with pytest.raises(ValidationError):
        SignPrediction(label=0, gloss="PAIN", confidence=0.9, stable=True)
    assert SignPrediction(label=11, gloss="PAIN", confidence=0.9, stable=True).gloss == "PAIN"

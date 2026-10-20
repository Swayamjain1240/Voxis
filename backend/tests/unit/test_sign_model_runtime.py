import asyncio

import pytest

from app.core.exceptions import FeatureUnavailableError
from app.services.sign_recognition.inference import SignInferenceService
from app.services.sign_recognition.model_loader import SignModelLoader


FRAMES = [[0.0] * 300 for _ in range(60)]


class FakeInput:
    name = "landmark_sequence"


class FakeOutput:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return [self.values]


class FakeSession:
    def get_inputs(self):
        return [FakeInput()]

    def run(self, _outputs, _inputs):
        logits = [0.0] * 12
        logits[11] = 8.0
        return [FakeOutput(logits)]


def test_loader_validates_shape_and_returns_probabilities():
    loader = SignModelLoader(session=FakeSession())
    probabilities = loader.predict(FRAMES)

    assert len(probabilities) == 12
    assert sum(probabilities) == pytest.approx(1.0)
    assert probabilities[11] > 0.9

    with pytest.raises(ValueError, match="60 frames"):
        loader.predict([[0.0] * 300])


def test_sign_inference_service_returns_canonical_prediction():
    service = SignInferenceService(enabled=True, loader=SignModelLoader(session=FakeSession()))
    result = asyncio.run(service.predict({"frames": FRAMES, "sequence_id": "seq-1"}))

    assert result.prediction.gloss == "PAIN"
    assert result.prediction.label == 11
    assert result.prediction.stable is True
    assert result.sequence_id == "seq-1"


def test_missing_sign_model_is_unavailable_without_fabricated_output():
    service = SignInferenceService(enabled=True, loader=SignModelLoader())
    with pytest.raises(FeatureUnavailableError) as error:
        asyncio.run(service.predict({"frames": FRAMES}))
    assert getattr(error.value, "code", None) == "SIGN_MODEL_UNAVAILABLE"

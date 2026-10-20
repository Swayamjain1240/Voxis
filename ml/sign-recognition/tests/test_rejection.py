import numpy as np
import pytest

from src.inference.rejection import RejectionPolicy, decide_prediction


def distribution(index: int, confidence: float) -> np.ndarray:
    values = np.full(12, (1.0 - confidence) / 11, dtype=np.float64)
    values[index] = confidence
    return values


def test_rejection_policy_accepts_clear_prediction_with_canonical_label():
    result = decide_prediction(distribution(11, 0.9))
    assert result.accepted is True
    assert result.gloss == "PAIN"
    assert result.label == 11
    assert result.reason == "accepted"


def test_rejection_policy_returns_unknown_for_low_or_ambiguous_predictions():
    low = decide_prediction(distribution(0, 0.2))
    assert low.gloss == "UNKNOWN"
    assert low.reason == "low_confidence"

    ambiguous = np.full(12, 1 / 12, dtype=np.float64)
    ambiguous[0] += 0.04
    ambiguous /= ambiguous.sum()
    result = decide_prediction(
        ambiguous,
        policy=RejectionPolicy(confidence_threshold=0.05, margin_threshold=0.05),
    )
    assert result.reason == "ambiguous"
    assert result.label == -1


def test_rejection_policy_validates_probability_contract():
    with pytest.raises(ValueError, match="sum to one"):
        decide_prediction(np.ones(12))
    with pytest.raises(ValueError, match="12 classes"):
        decide_prediction(np.ones(11) / 11)

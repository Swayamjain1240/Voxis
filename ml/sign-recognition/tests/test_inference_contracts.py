import numpy as np
import pytest

from src.contracts.sign_input import validate_sequence, validate_top_k
from src.inference.sign_detector import SignDetector


def test_validate_sequence_enforces_canonical_shape_and_finiteness():
    sequence = validate_sequence(np.zeros((60, 300), dtype=np.float32))
    assert sequence.flags.c_contiguous

    with pytest.raises(ValueError, match="canonical sign sequence"):
        validate_sequence(np.zeros((30, 300), dtype=np.float32))
    invalid = np.zeros((60, 300), dtype=np.float32)
    invalid[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        validate_sequence(invalid)


def test_detector_rejects_unknown_or_low_confidence_predictions():
    detector = SignDetector(confidence_threshold=0.6)

    unsupported = detector.detect("FEVER", 0.99)
    assert unsupported.gloss == "UNKNOWN"
    assert unsupported.reason == "unsupported_gloss"
    assert unsupported.label == -1

    uncertain = detector.detect("PAIN", 0.2)
    assert uncertain.gloss == "UNKNOWN"
    assert uncertain.reason == "low_confidence"

    accepted = detector.detect("PAIN", 0.95)
    assert accepted.accepted is True
    assert accepted.label == 11
    assert accepted.vocabulary_version == "1.0.0"


def test_top_k_is_bounded():
    assert validate_top_k(3) == 3
    with pytest.raises(ValueError):
        validate_top_k(0)
    with pytest.raises(ValueError):
        validate_top_k(11)

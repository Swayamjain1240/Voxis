import numpy as np
import pytest

from src.evaluation.calibration import (
    fit_temperature,
    negative_log_likelihood,
    softmax_logits,
)


def test_temperature_scaling_returns_normalized_probabilities():
    probabilities = softmax_logits(np.array([[2.0, 0.0], [0.0, 2.0]]), temperature=2.0)
    assert np.allclose(probabilities.sum(axis=1), 1.0)
    assert probabilities[0, 0] > probabilities[0, 1]


def test_temperature_fit_is_deterministic_and_improves_over_bad_scale():
    logits = np.array([[6.0, 0.0], [0.0, 6.0], [4.0, 0.0], [0.0, 4.0]])
    targets = np.array([0, 1, 0, 1])
    fitted = fit_temperature(logits, targets, minimum=0.5, maximum=3.0, steps=51)
    assert 0.5 <= fitted <= 3.0
    assert negative_log_likelihood(logits, targets, fitted) <= negative_log_likelihood(
        logits, targets, 3.0
    )


def test_calibration_rejects_invalid_temperature_and_logits():
    with pytest.raises(ValueError, match="positive"):
        softmax_logits(np.array([[1.0, 0.0]]), temperature=0)
    with pytest.raises(ValueError, match="finite"):
        fit_temperature(np.array([[np.nan, 0.0]]), np.array([0]))

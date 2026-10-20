import numpy as np
import pytest

from src.training.class_weights import inverse_frequency_weights


def test_inverse_frequency_weights_balance_present_classes():
    weights = inverse_frequency_weights([0, 0, 0, 1], 3)
    assert weights.dtype == np.float32
    assert weights[1] > weights[0]
    assert weights[2] == 0.0
    assert np.mean(weights[weights > 0]) == pytest.approx(1.0)


def test_class_weights_validate_labels():
    with pytest.raises(ValueError, match="class-index"):
        inverse_frequency_weights([[0]], 2)
    with pytest.raises(ValueError, match="class-index"):
        inverse_frequency_weights([2], 2)

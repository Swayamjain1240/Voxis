import numpy as np
import pytest

from src.evaluation.metrics import (
    balanced_accuracy,
    expected_calibration_error,
    macro_f1,
    multiclass_brier_score,
    top_k_indices,
)


def test_class_metrics_include_zero_support_classes():
    predictions = np.array([0, 0, 1])
    targets = np.array([0, 1, 1])
    assert balanced_accuracy(predictions, targets, 3) == pytest.approx(0.5)
    assert macro_f1(predictions, targets, 3) == pytest.approx(4 / 9)


def test_top_k_indices_are_sorted_by_confidence():
    probabilities = np.array([[0.1, 0.7, 0.2], [0.8, 0.1, 0.1]])
    assert top_k_indices(probabilities, 2).tolist() == [[1, 2], [0, 2]]


def test_calibration_and_brier_scores_are_bounded():
    probabilities = np.array([[0.9, 0.1], [0.4, 0.6]])
    targets = np.array([0, 1])
    assert 0.0 <= expected_calibration_error(probabilities, targets) <= 1.0
    assert multiclass_brier_score(probabilities, targets) == pytest.approx(0.17)


def test_metric_inputs_are_validated():
    with pytest.raises(ValueError, match="finite"):
        top_k_indices(np.array([[np.nan, 1.0]]))
    with pytest.raises(ValueError, match="bins"):
        expected_calibration_error(np.array([[1.0, 0.0]]), np.array([0]), bins=0)

import numpy as np
import pytest

from src.models.baseline import TemporalCentroidClassifier


def _sequences():
    values = np.zeros((6, 60, 300), dtype=np.float64)
    values[:3] += 1.0
    values[3:] -= 1.0
    return values


def test_temporal_centroid_baseline_separates_simple_classes():
    model = TemporalCentroidClassifier(num_classes=2).fit(
        _sequences(), [0, 0, 0, 1, 1, 1]
    )
    probabilities = model.predict_proba(_sequences())
    assert model.predict(_sequences()).tolist() == [0, 0, 0, 1, 1, 1]
    assert np.allclose(probabilities.sum(axis=1), 1.0)


def test_baseline_requires_canonical_input_shape():
    with pytest.raises(ValueError, match="60, 300"):
        TemporalCentroidClassifier(num_classes=2).fit(np.zeros((2, 4)), [0, 1])

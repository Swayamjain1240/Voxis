import pytest

from src.evaluation.benchmark import compare_to_baseline


def test_model_must_strictly_beat_baseline():
    result = compare_to_baseline(
        {"metrics": {"balanced_accuracy": 0.8}},
        {"metrics": {"balanced_accuracy": 0.7}},
    )
    assert result["beats_baseline"] is True
    assert result["delta"] == pytest.approx(0.1)


def test_benchmark_requires_numeric_metric():
    with pytest.raises(ValueError, match="numeric"):
        compare_to_baseline(
            {"metrics": {"balanced_accuracy": None}},
            {"metrics": {"balanced_accuracy": 0.7}},
        )

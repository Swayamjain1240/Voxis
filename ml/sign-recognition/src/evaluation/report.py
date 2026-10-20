from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence

import numpy as np

from src.evaluation.confusion_matrix import build_confusion_matrix
from src.evaluation.metrics import (
    accuracy,
    balanced_accuracy,
    expected_calibration_error,
    macro_f1,
    multiclass_brier_score,
    top_k_accuracy,
)


def _as_numpy(values: Iterable, *, name: str) -> np.ndarray:
    array = np.asarray(list(values))
    if array.ndim != 1:
        raise ValueError(f"{name} must be a one-dimensional sequence.")
    return array


def held_out_signer_metrics(
    predictions: Sequence[int],
    targets: Sequence[int],
    signer_ids: Sequence[str],
) -> dict[str, dict[str, float | int]]:
    predicted = _as_numpy(predictions, name="predictions")
    actual = _as_numpy(targets, name="targets")
    signers = _as_numpy(signer_ids, name="signer_ids")
    if not len(predicted) == len(actual) == len(signers):
        raise ValueError("predictions, targets, and signer_ids must have equal lengths.")
    report: dict[str, dict[str, float | int]] = {}
    for signer in sorted({str(value) for value in signers}):
        mask = signers == signer
        report[signer] = {
            "num_samples": int(mask.sum()),
            "accuracy": accuracy(predicted[mask], actual[mask]),
        }
    return report


def build_evaluation_report(
    predictions: Sequence[int],
    targets: Sequence[int],
    probabilities: Sequence[Sequence[float]],
    *,
    labels: Sequence[str],
    signer_ids: Sequence[str] | None = None,
    test_signers: Sequence[str] | None = None,
    metadata: Mapping[str, object] | None = None,
) -> dict[str, object]:
    predicted = _as_numpy(predictions, name="predictions").astype(int)
    actual = _as_numpy(targets, name="targets").astype(int)
    probability_array = np.asarray(probabilities, dtype=np.float64)
    if len(predicted) != len(actual) or len(actual) != len(probability_array):
        raise ValueError("predictions, targets, and probabilities must have equal lengths.")
    if probability_array.ndim != 2 or probability_array.shape[1] != len(labels):
        raise ValueError("probabilities must have one column per label.")
    if len(labels) == 0 or len(set(labels)) != len(labels):
        raise ValueError("labels must be a non-empty unique sequence.")

    matrix = build_confusion_matrix(predicted, actual, len(labels))
    report: dict[str, object] = {
        "metrics": {
            "accuracy": accuracy(predicted, actual),
            "balanced_accuracy": balanced_accuracy(predicted, actual, len(labels)),
            "macro_f1": macro_f1(predicted, actual, len(labels)),
            "top_3_accuracy": top_k_accuracy(
                probability_array,
                actual,
                k=min(3, len(labels)),
            ),
            "expected_calibration_error": expected_calibration_error(
                probability_array,
                actual,
            ),
            "multiclass_brier_score": multiclass_brier_score(
                probability_array,
                actual,
            ),
        },
        "num_test_samples": int(len(actual)),
        "labels": list(labels),
        "confusion_matrix": matrix.tolist(),
        "test_signers": sorted({str(value) for value in (test_signers or [])}),
    }
    if signer_ids is not None:
        report["signer_metrics"] = held_out_signer_metrics(
            predicted,
            actual,
            signer_ids,
        )
    if metadata:
        for key in ("model_version", "vocabulary_version", "preprocessing_version"):
            if key in metadata:
                report[key] = metadata[key]
    return report

from __future__ import annotations

import numpy as np


def accuracy(
    predictions,
    targets,
) -> float:

    if len(targets) == 0:
        return 0.0

    predictions = np.asarray(
        predictions
    )

    targets = np.asarray(
        targets
    )

    return float(
        np.mean(
            predictions
            == targets
        )
    )


def top_k_accuracy(
    probabilities,
    targets,
    k: int = 3,
) -> float:

    probabilities = np.asarray(
        probabilities
    )

    targets = np.asarray(
        targets
    )

    if len(targets) == 0:
        return 0.0

    top_k = np.argsort(
        probabilities,
        axis=1,
    )[:, -k:]

    hits = [
        target in row
        for target, row in zip(
            targets,
            top_k,
        )
    ]

    return float(
        np.mean(hits)
    )


def per_class_accuracy(
    predictions,
    targets,
    labels,
):
    predictions = np.asarray(
        predictions
    )

    targets = np.asarray(
        targets
    )

    result = {}

    for label in labels:
        mask = (
            targets == label
        )

        if not mask.any():
            result[str(label)] = 0.0
            continue

        result[str(label)] = float(
            np.mean(
                predictions[mask]
                == targets[mask]
            )
        )

    return result


def balanced_accuracy(
    predictions,
    targets,
    num_classes: int,
) -> float:
    """Mean recall across classes, including zero-support classes as zero."""
    predictions = np.asarray(predictions)
    targets = np.asarray(targets)
    if num_classes <= 0:
        raise ValueError("num_classes must be positive.")
    recalls = []
    for label in range(num_classes):
        mask = targets == label
        recalls.append(float(np.mean(predictions[mask] == label)) if mask.any() else 0.0)
    return float(np.mean(recalls))


def macro_f1(
    predictions,
    targets,
    num_classes: int,
) -> float:
    predictions = np.asarray(predictions)
    targets = np.asarray(targets)
    if num_classes <= 0:
        raise ValueError("num_classes must be positive.")
    scores = []
    for label in range(num_classes):
        true_positive = int(np.sum((predictions == label) & (targets == label)))
        false_positive = int(np.sum((predictions == label) & (targets != label)))
        false_negative = int(np.sum((predictions != label) & (targets == label)))
        denominator = 2 * true_positive + false_positive + false_negative
        scores.append(2 * true_positive / denominator if denominator else 0.0)
    return float(np.mean(scores))


def top_k_indices(probabilities, k: int = 3) -> np.ndarray:
    probabilities = np.asarray(probabilities, dtype=np.float64)
    if probabilities.ndim != 2 or not np.isfinite(probabilities).all():
        raise ValueError("probabilities must be a finite [samples, classes] matrix.")
    if not isinstance(k, int) or k < 1 or k > probabilities.shape[1]:
        raise ValueError("k must be between 1 and the number of classes.")
    return np.argsort(probabilities, axis=1)[:, -k:][:, ::-1]


def expected_calibration_error(
    probabilities,
    targets,
    bins: int = 10,
) -> float:
    """Compute confidence/accuracy gap over fixed confidence bins."""
    probabilities = np.asarray(probabilities, dtype=np.float64)
    targets = np.asarray(targets)
    if probabilities.ndim != 2 or len(targets) != len(probabilities):
        raise ValueError("probabilities and targets have incompatible shapes.")
    if not np.isfinite(probabilities).all() or not 1 <= bins <= 100:
        raise ValueError("probabilities must be finite and bins must be 1–100.")
    if len(targets) == 0:
        return 0.0
    predicted = probabilities.argmax(axis=1)
    confidence = probabilities.max(axis=1)
    edges = np.linspace(0.0, 1.0, bins + 1)
    error = 0.0
    for index in range(bins):
        lower, upper = edges[index], edges[index + 1]
        mask = (confidence > lower) & (confidence <= upper)
        if index == 0:
            mask = (confidence >= lower) & (confidence <= upper)
        if mask.any():
            error += float(mask.mean()) * abs(
                float(confidence[mask].mean())
                - float((predicted[mask] == targets[mask]).mean())
            )
    return error


def multiclass_brier_score(probabilities, targets) -> float:
    probabilities = np.asarray(probabilities, dtype=np.float64)
    targets = np.asarray(targets)
    if probabilities.ndim != 2 or len(targets) != len(probabilities):
        raise ValueError("probabilities and targets have incompatible shapes.")
    if not np.isfinite(probabilities).all():
        raise ValueError("probabilities must be finite.")
    if len(targets) == 0:
        return 0.0
    one_hot = np.zeros_like(probabilities)
    one_hot[np.arange(len(targets)), targets.astype(int)] = 1.0
    return float(np.mean(np.sum((probabilities - one_hot) ** 2, axis=1)))

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

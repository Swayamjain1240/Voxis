from __future__ import annotations

import numpy as np


def inverse_frequency_weights(
    labels,
    num_classes: int,
    *,
    absent_weight: float = 0.0,
) -> np.ndarray:
    """Return mean-one weights without allowing absent classes to explode."""
    if num_classes <= 0:
        raise ValueError("num_classes must be positive.")
    values = np.asarray(labels, dtype=np.int64)
    if values.ndim != 1 or np.any(values < 0) or np.any(values >= num_classes):
        raise ValueError("labels must be a one-dimensional class-index vector.")
    counts = np.bincount(values, minlength=num_classes).astype(np.float64)
    weights = np.full(num_classes, float(absent_weight), dtype=np.float64)
    present = counts > 0
    if present.any():
        weights[present] = len(values) / (present.sum() * counts[present])
        weights[present] /= weights[present].mean()
    return weights.astype(np.float32)

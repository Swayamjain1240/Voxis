from __future__ import annotations

import numpy as np


def _validate_logits_targets(logits, targets) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(logits, dtype=np.float64)
    labels = np.asarray(targets, dtype=np.int64)
    if values.ndim != 2 or values.shape[0] == 0:
        raise ValueError("logits must be a non-empty [samples, classes] matrix.")
    if len(labels) != len(values) or np.any(labels < 0) or np.any(labels >= values.shape[1]):
        raise ValueError("targets must match logits rows and class bounds.")
    if not np.isfinite(values).all():
        raise ValueError("logits must be finite.")
    return values, labels


def softmax_logits(logits, temperature: float = 1.0) -> np.ndarray:
    values = np.asarray(logits, dtype=np.float64)
    if not np.isfinite(values).all() or temperature <= 0:
        raise ValueError("logits must be finite and temperature must be positive.")
    shifted = values / temperature
    shifted -= shifted.max(axis=1, keepdims=True)
    exponentials = np.exp(shifted)
    return exponentials / exponentials.sum(axis=1, keepdims=True)


def negative_log_likelihood(logits, targets, temperature: float = 1.0) -> float:
    values, labels = _validate_logits_targets(logits, targets)
    probabilities = softmax_logits(values, temperature)
    return float(-np.log(np.clip(probabilities[np.arange(len(labels)), labels], 1e-12, 1.0)).mean())


def fit_temperature(
    logits,
    targets,
    *,
    minimum: float = 0.25,
    maximum: float = 4.0,
    steps: int = 151,
) -> float:
    """Select a scalar temperature using validation logits only."""
    if minimum <= 0 or maximum < minimum or steps < 2:
        raise ValueError("Temperature search bounds are invalid.")
    values, labels = _validate_logits_targets(logits, targets)
    candidates = np.linspace(minimum, maximum, steps)
    losses = [negative_log_likelihood(values, labels, float(candidate)) for candidate in candidates]
    return float(candidates[int(np.argmin(losses))])

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class TemporalCentroidClassifier:
    """Deterministic pooled-feature baseline for model comparisons.

    The baseline intentionally ignores temporal order and represents each
    sequence by its mean landmark frame. A trained temporal model must beat this
    score on the same signer-wise test split before it can be treated as useful.
    """

    num_classes: int
    centroids: np.ndarray | None = None
    class_counts: np.ndarray | None = None

    def fit(self, sequences, targets) -> "TemporalCentroidClassifier":
        pooled = _pool_sequences(sequences)
        labels = _validate_targets(targets, self.num_classes, len(pooled))
        self.centroids = np.zeros((self.num_classes, pooled.shape[1]), dtype=np.float64)
        self.class_counts = np.bincount(labels, minlength=self.num_classes)
        for label in range(self.num_classes):
            if self.class_counts[label]:
                self.centroids[label] = pooled[labels == label].mean(axis=0)
        if not np.any(self.class_counts):
            raise ValueError("Baseline requires at least one labeled sequence.")
        return self

    def predict_proba(self, sequences) -> np.ndarray:
        if self.centroids is None or self.class_counts is None:
            raise RuntimeError("Baseline must be fitted before prediction.")
        pooled = _pool_sequences(sequences)
        distances = ((pooled[:, None, :] - self.centroids[None, :, :]) ** 2).mean(axis=2)
        # Classes absent from training must not become accidental predictions.
        distances[:, self.class_counts == 0] = np.inf
        scores = -distances
        scores -= np.max(scores, axis=1, keepdims=True)
        probabilities = np.exp(scores)
        probabilities /= probabilities.sum(axis=1, keepdims=True)
        return probabilities

    def predict(self, sequences) -> np.ndarray:
        return self.predict_proba(sequences).argmax(axis=1)


def _pool_sequences(sequences) -> np.ndarray:
    values = np.asarray(sequences, dtype=np.float64)
    if values.ndim != 3 or values.shape[1:] != (60, 300):
        raise ValueError("sequences must have shape [samples, 60, 300].")
    if not np.isfinite(values).all():
        raise ValueError("sequences must contain only finite values.")
    return values.mean(axis=1)


def _validate_targets(targets, num_classes: int, sample_count: int) -> np.ndarray:
    labels = np.asarray(targets, dtype=np.int64)
    if labels.ndim != 1 or len(labels) != sample_count:
        raise ValueError("targets must align with the sequence count.")
    if num_classes <= 0 or np.any(labels < 0) or np.any(labels >= num_classes):
        raise ValueError("targets must be valid class indices.")
    return labels

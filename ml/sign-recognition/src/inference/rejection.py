from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.contracts.label_map import CanonicalLabelMap, load_label_map


@dataclass(frozen=True)
class RejectionPolicy:
    confidence_threshold: float = 0.60
    margin_threshold: float = 0.05

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0 and 1.")
        if not 0.0 <= self.margin_threshold <= 1.0:
            raise ValueError("margin_threshold must be between 0 and 1.")


@dataclass(frozen=True)
class PredictionDecision:
    label: int
    gloss: str
    confidence: float
    margin: float
    accepted: bool
    reason: str


def decide_prediction(
    probabilities,
    *,
    policy: RejectionPolicy | None = None,
    label_map: CanonicalLabelMap | None = None,
) -> PredictionDecision:
    values = np.asarray(probabilities, dtype=np.float64)
    if values.ndim != 1 or len(values) != 12 or not np.isfinite(values).all():
        raise ValueError("probabilities must be a finite vector of 12 classes.")
    if np.any(values < 0) or not np.isclose(values.sum(), 1.0, atol=1e-4):
        raise ValueError("probabilities must be non-negative and sum to one.")

    policy = policy or RejectionPolicy()
    canonical = label_map or load_label_map()
    ranking = np.argsort(values)[::-1]
    top_index = int(ranking[0])
    confidence = float(values[top_index])
    second = float(values[int(ranking[1])])
    margin = confidence - second
    if confidence < policy.confidence_threshold:
        return PredictionDecision(-1, "UNKNOWN", confidence, margin, False, "low_confidence")
    if margin < policy.margin_threshold:
        return PredictionDecision(-1, "UNKNOWN", confidence, margin, False, "ambiguous")
    return PredictionDecision(
        top_index,
        canonical.label_to_gloss[top_index],
        confidence,
        margin,
        True,
        "accepted",
    )

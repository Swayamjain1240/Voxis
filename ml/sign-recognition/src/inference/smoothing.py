from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass


@dataclass
class SmoothedPrediction:
    gloss: str
    confidence: float


class PredictionSmoother:
    """
    Majority-vote temporal smoothing for real-time predictions.
    """

    def __init__(
        self,
        window_size: int = 5,
        minimum_confidence: float = 0.60,
    ):
        if window_size <= 0:
            raise ValueError(
                "window_size must be positive."
            )

        self.window = deque(
            maxlen=window_size
        )

        self.minimum_confidence = (
            minimum_confidence
        )

    def update(
        self,
        gloss: str,
        confidence: float,
    ) -> SmoothedPrediction:

        if (
            confidence
            < self.minimum_confidence
        ):
            return SmoothedPrediction(
                gloss="UNKNOWN",
                confidence=confidence,
            )

        self.window.append(
            (
                gloss.upper(),
                confidence,
            )
        )

        counts = Counter(
            item[0]
            for item in self.window
        )

        winner, _ = (
            counts.most_common(1)[0]
        )

        winner_confidences = [
            score
            for item_gloss, score
            in self.window
            if item_gloss == winner
        ]

        confidence_value = (
            sum(
                winner_confidences
            )
            / len(
                winner_confidences
            )
        )

        return SmoothedPrediction(
            gloss=winner,
            confidence=confidence_value,
        )

    def reset(self):
        self.window.clear()

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SignDetection:
    gloss: str
    confidence: float
    accepted: bool
    reason: str


class SignDetector:
    """
    Converts frame/window predictions into accepted sign events.

    This stage is responsible for:
      - confidence threshold
      - UNKNOWN rejection
      - duplicate suppression
    """

    def __init__(
        self,
        confidence_threshold: float = 0.60,
    ):
        self.confidence_threshold = (
            confidence_threshold
        )

        self.last_emitted_gloss = None

    def detect(
        self,
        gloss: str,
        confidence: float,
    ) -> SignDetection:

        gloss = (
            str(gloss)
            .strip()
            .upper()
        )

        if not gloss:
            return SignDetection(
                gloss="UNKNOWN",
                confidence=confidence,
                accepted=False,
                reason="empty_gloss",
            )

        if confidence < (
            self.confidence_threshold
        ):
            return SignDetection(
                gloss="UNKNOWN",
                confidence=confidence,
                accepted=False,
                reason="low_confidence",
            )

        if (
            self.last_emitted_gloss
            == gloss
        ):
            return SignDetection(
                gloss=gloss,
                confidence=confidence,
                accepted=False,
                reason="duplicate",
            )

        self.last_emitted_gloss = gloss

        return SignDetection(
            gloss=gloss,
            confidence=confidence,
            accepted=True,
            reason="accepted",
        )

    def reset(self):
        self.last_emitted_gloss = None

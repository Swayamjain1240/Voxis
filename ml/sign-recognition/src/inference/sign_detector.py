from __future__ import annotations

from dataclasses import dataclass

import math

from src.contracts.label_map import load_label_map


@dataclass
class SignDetection:
    gloss: str
    confidence: float
    accepted: bool
    reason: str
    label: int = -1
    vocabulary_version: str = "1.0.0"


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
        label_map=None,
    ):
        if not math.isfinite(confidence_threshold) or not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0 and 1.")
        self.confidence_threshold = confidence_threshold
        self.label_map = label_map or load_label_map()

        self.last_emitted_gloss = None

    def detect(
        self,
        gloss: str,
        confidence: float,
    ) -> SignDetection:

        gloss = str(gloss).strip().upper()
        if not math.isfinite(float(confidence)) or not 0.0 <= float(confidence) <= 1.0:
            raise ValueError("confidence must be finite and between 0 and 1.")
        confidence = float(confidence)

        if not gloss:
            return SignDetection(
                gloss="UNKNOWN",
                confidence=confidence,
                accepted=False,
                reason="empty_gloss",
                vocabulary_version=self.label_map.version,
            )

        if gloss == "UNKNOWN" or gloss not in self.label_map.gloss_to_label:
            return SignDetection(
                gloss="UNKNOWN",
                confidence=confidence,
                accepted=False,
                reason="unsupported_gloss" if gloss != "UNKNOWN" else "unknown_prediction",
                vocabulary_version=self.label_map.version,
            )

        if confidence < (
            self.confidence_threshold
        ):
            return SignDetection(
                gloss="UNKNOWN",
                confidence=confidence,
                accepted=False,
                reason="low_confidence",
                vocabulary_version=self.label_map.version,
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
                label=self.label_map.gloss_to_label[gloss],
                vocabulary_version=self.label_map.version,
            )

        self.last_emitted_gloss = gloss

        return SignDetection(
            gloss=gloss,
            confidence=confidence,
            accepted=True,
            reason="accepted",
            label=self.label_map.gloss_to_label[gloss],
            vocabulary_version=self.label_map.version,
        )

    def reset(self):
        self.last_emitted_gloss = None

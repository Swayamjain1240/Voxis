from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from src.contracts.label_map import (
    SCHEMA_VERSION as VOCABULARY_VERSION,
    CanonicalLabelMap,
    load_label_map,
)


SCHEMA_VERSION = "1.0.0"
PREPROCESSING_VERSION = "1.0.0"
SEQUENCE_LENGTH = 60
INPUT_FEATURES = 300


@dataclass(frozen=True)
class ModelMetadata:
    model_version: str
    vocabulary_version: str = VOCABULARY_VERSION
    preprocessing_version: str = PREPROCESSING_VERSION
    sequence_length: int = SEQUENCE_LENGTH
    input_features: int = INPUT_FEATURES
    unknown_label: int = -1

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": SCHEMA_VERSION,
            "model_version": self.model_version,
            "vocabulary_version": self.vocabulary_version,
            "preprocessing_version": self.preprocessing_version,
            "sequence_length": self.sequence_length,
            "input_features": self.input_features,
            "unknown_label": self.unknown_label,
        }


def validate_checkpoint_metadata(
    checkpoint: Mapping[str, object],
    label_map: CanonicalLabelMap | None = None,
) -> ModelMetadata:
    canonical = label_map or load_label_map()
    required = {
        "schema_version", "model_version", "vocabulary_version",
        "preprocessing_version", "sequence_length", "input_features", "label_map",
        "unknown_label",
    }
    missing = sorted(required - set(checkpoint))
    if missing:
        raise ValueError(f"Checkpoint metadata is missing: {', '.join(missing)}")
    if checkpoint["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Checkpoint schema version is not supported.")
    if checkpoint["vocabulary_version"] != canonical.version:
        raise ValueError("Checkpoint vocabulary version does not match the shared map.")
    if checkpoint["preprocessing_version"] != PREPROCESSING_VERSION:
        raise ValueError("Checkpoint preprocessing version is not supported.")
    if checkpoint["label_map"] != canonical.gloss_to_label:
        raise ValueError("Checkpoint label map does not match the shared map.")
    if checkpoint["unknown_label"] != canonical.unknown_label:
        raise ValueError("Checkpoint unknown label does not match the shared map.")
    if checkpoint["sequence_length"] != SEQUENCE_LENGTH or checkpoint["input_features"] != INPUT_FEATURES:
        raise ValueError("Checkpoint input shape must be 60 frames by 300 features.")
    model_version = checkpoint["model_version"]
    if not isinstance(model_version, str) or not 1 <= len(model_version) <= 64:
        raise ValueError("Checkpoint model_version must be 1–64 characters.")
    return ModelMetadata(
        model_version=model_version,
        vocabulary_version=checkpoint["vocabulary_version"],
        preprocessing_version=checkpoint["preprocessing_version"],
        sequence_length=checkpoint["sequence_length"],
        input_features=checkpoint["input_features"],
        unknown_label=checkpoint["unknown_label"],
    )

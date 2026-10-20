from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping

from src.contracts.label_map import CanonicalLabelMap, load_label_map
from src.contracts.model_metadata import (
    INPUT_FEATURES,
    PREPROCESSING_VERSION,
    SEQUENCE_LENGTH,
    VOCABULARY_VERSION,
)


MODEL_CONFIG_VERSION = "1.0.0"
SUPPORTED_ARCHITECTURES = frozenset({"transformer", "conformer"})


@dataclass(frozen=True)
class ModelConfig:
    model_version: str = "sign-transformer-0.1.0"
    architecture: str = "transformer"
    input_features: int = INPUT_FEATURES
    sequence_length: int = SEQUENCE_LENGTH
    num_classes: int = 12
    d_model: int = 256
    num_heads: int = 8
    num_layers: int = 4
    feedforward_dim: int = 1024
    dropout: float = 0.10
    vocabulary_version: str = VOCABULARY_VERSION
    preprocessing_version: str = PREPROCESSING_VERSION

    def as_dict(self) -> dict[str, object]:
        return {"config_version": MODEL_CONFIG_VERSION, **asdict(self)}

    def validate(self, label_map: CanonicalLabelMap | None = None) -> "ModelConfig":
        canonical = label_map or load_label_map()
        if self.architecture not in SUPPORTED_ARCHITECTURES:
            raise ValueError(f"Unsupported model architecture: {self.architecture}")
        if self.input_features != INPUT_FEATURES or self.sequence_length != SEQUENCE_LENGTH:
            raise ValueError("Model input must remain 60 frames by 300 features.")
        if self.num_classes != len(canonical.gloss_to_label):
            raise ValueError("Model class count must match the canonical vocabulary.")
        if self.vocabulary_version != canonical.version:
            raise ValueError("Model vocabulary version does not match the shared map.")
        if self.preprocessing_version != PREPROCESSING_VERSION:
            raise ValueError("Model preprocessing version is not supported.")
        if self.d_model <= 0 or self.num_heads <= 0 or self.num_layers <= 0:
            raise ValueError("Model dimensions must be positive.")
        if self.d_model % self.num_heads:
            raise ValueError("d_model must be divisible by num_heads.")
        if not 0.0 <= self.dropout < 1.0:
            raise ValueError("Model dropout must be between 0 and 1.")
        if not isinstance(self.model_version, str) or not 1 <= len(self.model_version) <= 64:
            raise ValueError("model_version must be 1–64 characters.")
        return self


def model_config_from_mapping(
    payload: Mapping[str, object],
    label_map: CanonicalLabelMap | None = None,
) -> ModelConfig:
    values = dict(payload)
    values.pop("config_version", None)
    config = ModelConfig(**values)
    return config.validate(label_map)

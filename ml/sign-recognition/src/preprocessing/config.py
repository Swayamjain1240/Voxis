from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np


PREPROCESSING_VERSION = "1.0.0"
TARGET_SEQUENCE_LENGTH = 60
FEATURES_PER_FRAME = 300
DEFAULT_AUGMENTATION_SEED = 42


@dataclass(frozen=True)
class PreprocessingConfig:
    version: str = PREPROCESSING_VERSION
    target_sequence_length: int = TARGET_SEQUENCE_LENGTH
    features_per_frame: int = FEATURES_PER_FRAME
    augmentation_seed: int = DEFAULT_AUGMENTATION_SEED

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)

    def validate_input(self, sequence: np.ndarray) -> np.ndarray:
        array = np.asarray(sequence, dtype=np.float32)
        if array.ndim != 2 or array.shape[1] != self.features_per_frame:
            raise ValueError(
                f"Expected raw sequence [frames, {self.features_per_frame}], got {array.shape}."
            )
        if array.shape[0] == 0:
            raise ValueError("Raw sequence must contain at least one frame.")
        return array

    def validate_output(self, sequence: np.ndarray) -> np.ndarray:
        array = np.asarray(sequence, dtype=np.float32)
        expected_shape = (self.target_sequence_length, self.features_per_frame)
        if array.shape != expected_shape:
            raise ValueError(f"Expected prepared sequence {expected_shape}, got {array.shape}.")
        if not np.isfinite(array).all():
            raise ValueError("Prepared sequence must contain only finite values.")
        return array

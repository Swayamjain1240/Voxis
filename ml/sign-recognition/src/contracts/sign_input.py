from __future__ import annotations

import numpy as np


SEQUENCE_LENGTH = 60
FEATURES_PER_FRAME = 300


def validate_sequence(
    sequence,
    *,
    sequence_length: int = SEQUENCE_LENGTH,
    features_per_frame: int = FEATURES_PER_FRAME,
) -> np.ndarray:
    array = np.asarray(sequence, dtype=np.float32)
    expected_shape = (sequence_length, features_per_frame)
    if array.shape != expected_shape:
        raise ValueError(
            f"Expected canonical sign sequence {expected_shape}, got {array.shape}."
        )
    if not np.isfinite(array).all():
        raise ValueError("Sign sequence must contain only finite values.")
    return np.ascontiguousarray(array)


def validate_top_k(top_k: int, *, maximum: int = 10) -> int:
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= maximum:
        raise ValueError(f"top_k must be an integer between 1 and {maximum}.")
    return top_k

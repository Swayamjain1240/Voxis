from __future__ import annotations

import numpy as np


def gaussian_jitter(
    sequence: np.ndarray,
    std: float = 0.005,
    seed: int | None = None,
) -> np.ndarray:

    rng = np.random.default_rng(
        seed
    )

    array = np.asarray(
        sequence,
        dtype=np.float32,
    )

    noise = rng.normal(
        0.0,
        std,
        size=array.shape,
    ).astype(np.float32)

    return array + noise


def temporal_crop(
    sequence: np.ndarray,
    crop_ratio: float = 0.90,
    seed: int | None = None,
) -> np.ndarray:

    array = np.asarray(
        sequence,
        dtype=np.float32,
    )

    if not 0 < crop_ratio <= 1:
        raise ValueError(
            "crop_ratio must be in (0, 1]."
        )

    if crop_ratio == 1:
        return array.copy()

    length = len(array)

    crop_length = max(
        2,
        int(length * crop_ratio),
    )

    if crop_length >= length:
        return array.copy()

    rng = np.random.default_rng(
        seed
    )

    start = int(
        rng.integers(
            0,
            length - crop_length + 1,
        )
    )

    return array[
        start:start + crop_length
    ]


def augment_sequence(
    sequence: np.ndarray,
    jitter_std: float = 0.003,
    seed: int | None = None,
) -> np.ndarray:

    cropped = temporal_crop(
        sequence,
        crop_ratio=0.95,
        seed=seed,
    )

    return gaussian_jitter(
        cropped,
        std=jitter_std,
        seed=seed,
    )

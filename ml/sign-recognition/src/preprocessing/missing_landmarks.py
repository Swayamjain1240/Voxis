from __future__ import annotations

import numpy as np


def replace_invalid_values(
    sequence: np.ndarray,
    fill_value: float = 0.0,
) -> np.ndarray:
    array = np.asarray(
        sequence,
        dtype=np.float32,
    ).copy()

    return np.nan_to_num(
        array,
        nan=fill_value,
        posinf=fill_value,
        neginf=fill_value,
    )


def interpolate_temporal_gaps(
    sequence: np.ndarray,
) -> np.ndarray:
    """
    Linearly interpolates missing values across time.

    Remaining values that cannot be interpolated are zero-filled.
    """

    array = np.asarray(
        sequence,
        dtype=np.float32,
    ).copy()

    if array.ndim != 2:
        raise ValueError(
            "Expected [frames, features]."
        )

    frame_count = array.shape[0]

    if frame_count == 0:
        return array

    for feature_index in range(
        array.shape[1]
    ):
        column = array[
            :,
            feature_index,
        ]

        valid = np.isfinite(column)

        if valid.all():
            continue

        if not valid.any():
            column[:] = 0.0
            continue

        valid_indices = np.flatnonzero(
            valid
        )

        column[:] = np.interp(
            np.arange(frame_count),
            valid_indices,
            column[valid],
        )

    return array


def clean_landmarks(
    sequence: np.ndarray,
) -> np.ndarray:
    array = replace_invalid_values(
        sequence
    )

    return interpolate_temporal_gaps(
        array
    )

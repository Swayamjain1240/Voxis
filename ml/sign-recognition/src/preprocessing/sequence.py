from __future__ import annotations

import numpy as np


def pad_sequence(
    sequence: np.ndarray,
    target_length: int = 60,
) -> np.ndarray:

    array = np.asarray(
        sequence,
        dtype=np.float32,
    )

    if array.ndim != 2:
        raise ValueError(
            "Expected [frames, features]."
        )

    if target_length <= 0:
        raise ValueError(
            "target_length must be positive."
        )

    if len(array) == target_length:
        return array.copy()

    if len(array) == 0:
        return np.zeros(
            (
                target_length,
                array.shape[1],
            ),
            dtype=np.float32,
        )

    if len(array) > target_length:
        indices = np.linspace(
            0,
            len(array) - 1,
            target_length,
        ).astype(int)

        return array[indices]

    padding = np.repeat(
        array[-1:],
        target_length - len(array),
        axis=0,
    )

    return np.concatenate(
        [
            array,
            padding,
        ],
        axis=0,
    )


def resample_sequence(
    sequence: np.ndarray,
    target_length: int = 60,
) -> np.ndarray:
    """
    Temporal resampling with linear interpolation.
    """

    array = np.asarray(
        sequence,
        dtype=np.float32,
    )

    if len(array) == 0:
        return pad_sequence(
            array,
            target_length,
        )

    if len(array) == target_length:
        return array.copy()

    old_positions = np.linspace(
        0.0,
        1.0,
        len(array),
    )

    new_positions = np.linspace(
        0.0,
        1.0,
        target_length,
    )

    result = np.empty(
        (
            target_length,
            array.shape[1],
        ),
        dtype=np.float32,
    )

    for feature_index in range(
        array.shape[1]
    ):
        result[
            :,
            feature_index,
        ] = np.interp(
            new_positions,
            old_positions,
            array[
                :,
                feature_index,
            ],
        )

    return result


def prepare_sequence(
    sequence: np.ndarray,
    target_length: int = 60,
) -> np.ndarray:

    if len(sequence) < target_length:
        return pad_sequence(
            sequence,
            target_length,
        )

    return resample_sequence(
        sequence,
        target_length,
    )

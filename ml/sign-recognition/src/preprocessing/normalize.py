from __future__ import annotations

import numpy as np


LEFT_SHOULDER_INDEX = 21 + 21 + 11
RIGHT_SHOULDER_INDEX = 21 + 21 + 12

FEATURES_PER_POINT = 4


def normalize_landmarks(
    sequence: np.ndarray,
) -> np.ndarray:
    """
    Normalizes every frame relative to the midpoint of
    the shoulders and scales by shoulder distance.

    Landmark indexing:
        0..20    left hand
        21..41   right hand
        42..74   pose

    Pose:
        11 = left shoulder
        12 = right shoulder
    """

    array = np.asarray(
        sequence,
        dtype=np.float32,
    ).copy()

    if array.ndim != 2:
        raise ValueError(
            "Expected sequence shape [frames, features]."
        )

    expected_features = (
        75 * FEATURES_PER_POINT
    )

    if array.shape[1] != expected_features:
        raise ValueError(
            f"Expected {expected_features} features, "
            f"got {array.shape[1]}."
        )

    landmarks = array.reshape(
        array.shape[0],
        75,
        FEATURES_PER_POINT,
    )

    left_shoulder = landmarks[
        :,
        32,
        :3,
    ]

    right_shoulder = landmarks[
        :,
        33,
        :3,
    ]

    center = (
        left_shoulder
        + right_shoulder
    ) / 2.0

    shoulder_distance = np.linalg.norm(
        left_shoulder
        - right_shoulder,
        axis=-1,
        keepdims=True,
    )

    shoulder_distance = np.maximum(
        shoulder_distance,
        1e-4,
    )

    xyz = (
        landmarks[:, :, :3]
        - center[:, None, :]
    )

    xyz /= shoulder_distance[
        :,
        None,
        :,
    ]

    landmarks[
        :,
        :,
        :3,
    ] = xyz

    return landmarks.reshape(
        array.shape[0],
        expected_features,
    )

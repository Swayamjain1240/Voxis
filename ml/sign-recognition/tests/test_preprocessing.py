import numpy as np

from src.preprocessing.missing_landmarks import (
    clean_landmarks,
)
from src.preprocessing.sequence import (
    prepare_sequence,
)
from src.preprocessing.normalize import (
    normalize_landmarks,
)


def test_sequence_prepare():
    sequence = np.random.rand(
        30,
        300,
    ).astype(
        np.float32
    )

    result = prepare_sequence(
        sequence,
        60,
    )

    assert result.shape == (
        60,
        300,
    )


def test_normalization_shape():
    sequence = np.random.rand(
        60,
        300,
    ).astype(
        np.float32
    )

    result = normalize_landmarks(
        sequence
    )

    assert result.shape == (
        60,
        300,
    )


def test_invalid_values_cleaned():
    sequence = np.zeros(
        (
            60,
            300,
        ),
        dtype=np.float32,
    )

    sequence[2, 10] = np.nan
    sequence[5, 20] = np.inf

    result = clean_landmarks(
        sequence
    )

    assert np.isfinite(
        result
    ).all()

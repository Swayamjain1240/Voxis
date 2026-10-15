import numpy as np
import pytest

from src.preprocessing.missing_landmarks import (
    clean_landmarks,
)
from src.preprocessing.sequence import (
    prepare_sequence,
)
from src.preprocessing.normalize import (
    LEFT_SHOULDER_INDEX,
    RIGHT_SHOULDER_INDEX,
    normalize_landmarks,
)
from src.preprocessing.missing_landmarks import interpolate_temporal_gaps
from src.preprocessing.augmentation import augment_sequence
from src.preprocessing.config import PreprocessingConfig


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


def test_normalization_uses_pose_shoulder_indices():
    sequence = np.zeros((1, 300), dtype=np.float32)
    landmarks = sequence.reshape(1, 75, 4)
    landmarks[0, LEFT_SHOULDER_INDEX, :3] = [0.0, 0.0, 0.0]
    landmarks[0, RIGHT_SHOULDER_INDEX, :3] = [2.0, 0.0, 0.0]
    landmarks[0, 0, :3] = [1.0, 0.0, 0.0]

    result = normalize_landmarks(sequence).reshape(1, 75, 4)

    assert np.allclose(result[0, 0, :3], [0.0, 0.0, 0.0])
    assert np.allclose(
        result[0, LEFT_SHOULDER_INDEX, :3],
        [-0.5, 0.0, 0.0],
    )
    assert np.allclose(
        result[0, RIGHT_SHOULDER_INDEX, :3],
        [0.5, 0.0, 0.0],
    )


def test_temporal_gaps_are_interpolated_before_fill():
    sequence = np.array([[0.0], [np.nan], [2.0]], dtype=np.float32)

    result = interpolate_temporal_gaps(sequence)

    assert np.allclose(result[:, 0], [0.0, 1.0, 2.0])


def test_unrecoverable_temporal_gaps_are_zero_filled():
    sequence = np.array([[np.nan], [np.inf]], dtype=np.float32)

    result = interpolate_temporal_gaps(sequence)

    assert np.array_equal(result[:, 0], [0.0, 0.0])


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


def test_preprocessing_config_rejects_empty_or_wrong_feature_inputs():
    config = PreprocessingConfig()

    with pytest.raises(ValueError, match="at least one frame"):
        config.validate_input(np.zeros((0, 300), dtype=np.float32))
    with pytest.raises(ValueError, match="300"):
        config.validate_input(np.zeros((5, 299), dtype=np.float32))


def test_augmentation_is_reproducible_with_a_seed():
    sequence = np.ones((8, 300), dtype=np.float32)
    first = augment_sequence(sequence, seed=7)
    second = augment_sequence(sequence, seed=7)

    assert np.array_equal(first, second)


def test_preprocessing_config_validates_prepared_output():
    config = PreprocessingConfig()
    valid = np.zeros((60, 300), dtype=np.float32)
    assert config.validate_output(valid).shape == (60, 300)

    invalid = valid.copy()
    invalid[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        config.validate_output(invalid)

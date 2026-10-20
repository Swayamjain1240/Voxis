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
from scripts.prepare_dataset import prepare_manifest, stable_sample_seed


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


def test_manifest_preparation_is_reproducible_and_writes_training_manifest(tmp_path):
    source = tmp_path / "raw" / "PAIN" / "signer-1" / "sample-1.npy"
    source.parent.mkdir(parents=True)
    np.save(source, np.ones((30, 300), dtype=np.float32))
    manifest = tmp_path / "input.csv"
    manifest.write_text(
        "sample_id,sequence_path,label,signer_id\n"
        f"sample-1,{source},PAIN,signer-1\n",
        encoding="utf-8",
    )
    output = tmp_path / "processed"
    output_manifest = output / "manifest.csv"

    rows = prepare_manifest(
        manifest,
        None,
        output,
        output_manifest,
        sequence_length=60,
        augment=True,
        seed=7,
    )

    prepared = np.load(rows[0]["sequence_path"], allow_pickle=False)
    assert prepared.shape == (60, 300)
    assert rows[0]["preprocessing_version"] == "1.0.0"
    assert int(rows[0]["augmentation_seed"]) == stable_sample_seed(7, "sample-1")
    assert output_manifest.exists()
    assert (output / "preprocessing_config.json").exists()
    assert (output / "rejected.csv").exists()


def test_manifest_preparation_reports_invalid_sequence_without_fabricating_output(tmp_path):
    source = tmp_path / "raw" / "PAIN" / "signer-1" / "bad.npy"
    source.parent.mkdir(parents=True)
    np.save(source, np.ones((30, 299), dtype=np.float32))
    manifest = tmp_path / "input.csv"
    manifest.write_text(
        "sample_id,sequence_path,label,signer_id\n"
        f"bad,{source},PAIN,signer-1\n",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="No valid sequences"):
        prepare_manifest(
            manifest,
            None,
            tmp_path / "processed",
            tmp_path / "processed" / "manifest.csv",
            sequence_length=60,
            augment=False,
            seed=42,
        )
    rejection = (tmp_path / "processed" / "rejected.csv").read_text(encoding="utf-8")
    assert "bad" in rejection
    assert "299" in rejection

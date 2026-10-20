import csv

import pytest

from src.datasets.manifest import (
    ManifestValidationError,
    load_manifest,
    validate_extraction_rows,
    validate_manifest_rows,
    write_split_manifests,
)
from src.datasets.splitter import signer_wise_split


def row(sample_id, signer, label="PAIN", **extra):
    return {
        "sample_id": sample_id,
        "sequence_path": f"processed/{signer}/{sample_id}.npy",
        "label": label,
        "signer_id": signer,
        **extra,
    }


def test_manifest_normalizes_labels_and_requires_known_signers():
    result = validate_manifest_rows([row("a", "s1", label="pain")])
    assert result[0]["label"] == "PAIN"

    with pytest.raises(ManifestValidationError, match="known signer"):
        validate_manifest_rows([row("a", "unknown")])


def test_manifest_rejects_cross_signer_duplicate_groups():
    rows = [
        row("a", "s1", content_hash="same-bytes"),
        row("b", "s2", content_hash="same-bytes"),
    ]
    with pytest.raises(ManifestValidationError, match="cross signer"):
        validate_manifest_rows(rows)


def test_split_keeps_signers_and_duplicate_groups_isolated():
    rows = [row(f"{signer}-sample", signer) for signer in ("s1", "s2", "s3")]
    split = signer_wise_split(rows)
    assert set(split["train_signers"]).isdisjoint(split["validation_signers"])
    assert set(split["train_signers"]).isdisjoint(split["test_signers"])
    assert set(split["validation_signers"]).isdisjoint(split["test_signers"])


def test_csv_loader_rejects_missing_columns(tmp_path):
    path = tmp_path / "manifest.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sample_id", "label"])
        writer.writerow(["a", "PAIN"])

    with pytest.raises(ManifestValidationError, match="missing required columns"):
        load_manifest(path)


def test_extraction_manifest_uses_video_path_until_sequence_exists():
    rows = validate_extraction_rows([
        {
            "sample_id": "sample-1",
            "video_path": "raw/PAIN/signer-1/sample-1.mp4",
            "label": "pain",
            "signer_id": "signer-1",
        }
    ])
    assert rows[0]["sequence_path"] == rows[0]["video_path"]


def test_extraction_manifest_rejects_unknown_signers_and_labels():
    with pytest.raises(ManifestValidationError, match="known signer"):
        validate_extraction_rows([
            {
                "sample_id": "sample-1",
                "video_path": "raw/PAIN/unknown/sample-1.mp4",
                "label": "PAIN",
                "signer_id": "unknown",
            }
        ])


def test_split_manifests_write_signer_metadata_and_csvs(tmp_path):
    rows = [row(f"{signer}-sample", signer) for signer in ("s1", "s2", "s3")]
    split = signer_wise_split(rows)
    paths = write_split_manifests(split, tmp_path / "splits")

    assert set(paths) == {"train", "validation", "test"}
    assert all(path.exists() for path in paths.values())
    metadata = (tmp_path / "splits" / "split_metadata.json").read_text(encoding="utf-8")
    assert '"strategy": "signer_wise"' in metadata
    with pytest.raises(ManifestValidationError, match="Unknown canonical label"):
        validate_extraction_rows([
            {
                "sample_id": "sample-1",
                "video_path": "raw/OTHER/signer-1/sample-1.mp4",
                "label": "OTHER",
                "signer_id": "signer-1",
            }
        ])

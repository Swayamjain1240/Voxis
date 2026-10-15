import csv

import pytest

from src.datasets.manifest import ManifestValidationError, load_manifest, validate_manifest_rows
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

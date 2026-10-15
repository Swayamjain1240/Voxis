from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Mapping

from src.contracts.label_map import CanonicalLabelMap, load_label_map


REQUIRED_COLUMNS = frozenset({
    "sample_id",
    "sequence_path",
    "label",
    "signer_id",
})
EXTRACTION_REQUIRED_COLUMNS = frozenset({
    "sample_id",
    "video_path",
    "label",
    "signer_id",
})


class ManifestValidationError(ValueError):
    """Raised when a training manifest cannot support safe evaluation."""


def duplicate_key(row: Mapping[str, str]) -> str:
    for field in ("duplicate_group", "content_hash", "source_id", "source_path", "video_path"):
        value = str(row.get(field, "")).strip()
        if value:
            return f"{field}:{value.casefold()}"
    return f"sequence_path:{str(row.get('sequence_path', '')).strip().casefold()}"


def validate_manifest_rows(
    rows: Iterable[Mapping[str, str]],
    label_map: CanonicalLabelMap | None = None,
) -> list[dict[str, str]]:
    canonical = label_map or load_label_map()
    normalized = []
    seen_samples: set[str] = set()
    seen_sequences: set[str] = set()
    duplicate_signers: dict[str, set[str]] = {}

    for row_number, row in enumerate(rows, start=2):
        sample_id = str(row.get("sample_id", "")).strip()
        sequence_path = str(row.get("sequence_path", "")).strip()
        label = str(row.get("label", "")).strip().upper()
        signer_id = str(row.get("signer_id", "")).strip()
        if not sample_id or not sequence_path or not label or not signer_id:
            raise ManifestValidationError(
                f"Manifest row {row_number} requires sample_id, sequence_path, label, and signer_id."
            )
        if signer_id.casefold() == "unknown":
            raise ManifestValidationError("Signer-wise evaluation requires a known signer_id.")
        if sample_id in seen_samples:
            raise ManifestValidationError(f"Duplicate sample_id: {sample_id}")
        if sequence_path.casefold() in seen_sequences:
            raise ManifestValidationError(f"Duplicate sequence_path: {sequence_path}")
        if label not in canonical.gloss_to_label:
            raise ManifestValidationError(f"Unknown canonical label: {label}")

        item = {str(key): str(value).strip() for key, value in row.items()}
        item.update({
            "sample_id": sample_id,
            "sequence_path": sequence_path,
            "label": label,
            "signer_id": signer_id,
        })
        key = duplicate_key(item)
        duplicate_signers.setdefault(key, set()).add(signer_id)
        seen_samples.add(sample_id)
        seen_sequences.add(sequence_path.casefold())
        normalized.append(item)

    cross_signer_duplicates = {
        key: signers
        for key, signers in duplicate_signers.items()
        if len(signers) > 1
    }
    if cross_signer_duplicates:
        details = ", ".join(
            f"{key} ({sorted(signers)})"
            for key, signers in sorted(cross_signer_duplicates.items())
        )
        raise ManifestValidationError(
            f"Duplicate content/source groups cross signer boundaries: {details}"
        )
    return normalized


def load_manifest(
    path: str | Path,
    label_map: CanonicalLabelMap | None = None,
) -> list[dict[str, str]]:
    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or ())
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise ManifestValidationError(
                f"Manifest is missing required columns: {sorted(missing)}"
            )
        return validate_manifest_rows(reader, label_map=label_map)


def validate_extraction_rows(
    rows: Iterable[Mapping[str, str]],
    label_map: CanonicalLabelMap | None = None,
) -> list[dict[str, str]]:
    """Validate the video manifest used before sequence extraction."""
    prepared = []
    for row_number, row in enumerate(rows, start=2):
        item = {str(key): str(value).strip() for key, value in row.items()}
        missing = [
            field for field in sorted(EXTRACTION_REQUIRED_COLUMNS)
            if not item.get(field)
        ]
        if missing:
            raise ManifestValidationError(
                f"Extraction manifest row {row_number} requires: {', '.join(missing)}."
            )
        # A source path acts as the temporary sequence identity until output exists.
        item["sequence_path"] = item["video_path"]
        prepared.append(item)
    return validate_manifest_rows(prepared, label_map=label_map)


def load_extraction_manifest(
    path: str | Path,
    label_map: CanonicalLabelMap | None = None,
) -> list[dict[str, str]]:
    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or ())
        missing = EXTRACTION_REQUIRED_COLUMNS - columns
        if missing:
            raise ManifestValidationError(
                f"Extraction manifest is missing required columns: {sorted(missing)}"
            )
        return validate_extraction_rows(reader, label_map=label_map)

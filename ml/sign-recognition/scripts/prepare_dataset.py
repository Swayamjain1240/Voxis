from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

import numpy as np

from src.preprocessing.augmentation import (
    augment_sequence,
)
from src.preprocessing.config import (
    DEFAULT_AUGMENTATION_SEED,
    PreprocessingConfig,
)
from src.datasets.manifest import load_manifest, validate_manifest_rows
from src.preprocessing.missing_landmarks import (
    clean_landmarks,
)
from src.preprocessing.normalize import (
    normalize_landmarks,
)
from src.preprocessing.sequence import (
    prepare_sequence,
)


def process_file(
    source: Path,
    destination: Path,
    sequence_length: int,
    augment: bool,
    seed: int = DEFAULT_AUGMENTATION_SEED,
    config: PreprocessingConfig | None = None,
):
    config = config or PreprocessingConfig(
        target_sequence_length=sequence_length,
        augmentation_seed=seed,
    )
    sequence = config.validate_input(np.load(source, allow_pickle=False))

    sequence = clean_landmarks(
        sequence
    )

    sequence = normalize_landmarks(
        sequence
    )

    if augment:
        sequence = augment_sequence(
            sequence,
            seed=seed,
        )

    sequence = prepare_sequence(
        sequence,
        sequence_length,
    )
    sequence = config.validate_output(sequence)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    np.save(
        destination,
        sequence.astype(
            np.float32
        ),
    )


def stable_sample_seed(base_seed: int, sample_id: str) -> int:
    digest = hashlib.sha256(sample_id.encode("utf-8")).digest()
    return (int(base_seed) + int.from_bytes(digest[:4], "big")) % (2**32)


def _safe_component(value: str, field: str) -> str:
    component = str(value).strip()
    if (
        not component
        or component in {".", ".."}
        or "/" in component
        or "\\" in component
    ):
        raise ValueError(f"Manifest {field} must be a safe path component.")
    return component


def _rows_from_directory(root: Path) -> list[dict[str, str]]:
    rows = []
    for source in sorted(root.rglob("*.npy")):
        relative = source.relative_to(root)
        if len(relative.parts) < 3:
            raise ValueError(
                "Directory input must use label/signer/sample.npy layout."
            )
        rows.append({
            "sample_id": source.stem,
            "sequence_path": str(source),
            "label": relative.parts[-3].upper(),
            "signer_id": relative.parts[-2],
        })
    return validate_manifest_rows(rows)


def prepare_manifest(
    manifest_path: Path | None,
    input_root: Path | None,
    output_root: Path,
    output_manifest: Path,
    *,
    sequence_length: int,
    augment: bool,
    seed: int,
) -> list[dict[str, str]]:
    if manifest_path:
        rows = load_manifest(manifest_path)
        manifest_base = manifest_path.parent
    elif input_root:
        rows = _rows_from_directory(input_root)
        manifest_base = Path.cwd()
    else:
        raise ValueError("Provide either a source manifest or an input directory.")
    if not rows:
        raise RuntimeError("No source sequences were found.")

    config = PreprocessingConfig(
        target_sequence_length=sequence_length,
        augmentation_seed=seed,
    )
    prepared_rows = []

    for row in rows:
        sample_id = _safe_component(row["sample_id"], "sample_id")
        label = _safe_component(row["label"].upper(), "label")
        signer_id = _safe_component(row["signer_id"], "signer_id")
        source_path = Path(row["sequence_path"])
        if not source_path.is_absolute():
            source_path = manifest_base / source_path

        destination = output_root / label / signer_id / f"{sample_id}.npy"
        sample_seed = stable_sample_seed(seed, sample_id)
        process_file(
            source_path,
            destination,
            sequence_length,
            augment,
            seed=sample_seed,
            config=config,
        )

        prepared_row = dict(row)
        prepared_row.update({
            "sample_id": sample_id,
            "sequence_path": str(destination),
            "source_sequence_path": str(source_path),
            "source_path": str(source_path),
            "label": label,
            "signer_id": signer_id,
            "preprocessing_version": config.version,
            "augmentation_seed": str(sample_seed) if augment else "",
        })
        prepared_rows.append(prepared_row)

    prepared_rows = validate_manifest_rows(prepared_rows)
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["sample_id", "sequence_path", "label", "signer_id"]
    extras = sorted(
        {key for row in prepared_rows for key in row}
        - set(fieldnames)
    )
    with output_manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames + extras)
        writer.writeheader()
        writer.writerows(prepared_rows)
    return prepared_rows


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Prepare raw extracted landmark arrays."
        )
    )

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--manifest", type=Path)
    source_group.add_argument("--input", type=Path)

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--sequence-length",
        type=int,
        default=60,
    )

    parser.add_argument(
        "--augment",
        action="store_true",
    )

    parser.add_argument(
        "--output-manifest",
        type=Path,
        help="Prepared manifest path; defaults to <output>/manifest.csv.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_AUGMENTATION_SEED,
        help="Stable seed used when augmentation is enabled.",
    )

    args = parser.parse_args()

    output_manifest = args.output_manifest or args.output / "manifest.csv"
    prepared_rows = prepare_manifest(
        args.manifest,
        args.input,
        args.output,
        output_manifest,
        sequence_length=args.sequence_length,
        augment=args.augment,
        seed=args.seed,
    )

    for index, row in enumerate(prepared_rows, start=1):
        print(f"[{index}/{len(prepared_rows)}] prepared {row['sample_id']}")

    print(
        f"Prepared {len(prepared_rows)} sequences. Manifest: {output_manifest}"
    )


if __name__ == "__main__":
    main()

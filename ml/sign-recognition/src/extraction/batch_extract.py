from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from mediapipe_extractor import (
    MediaPipeExtractor,
)
from src.datasets.manifest import (
    load_extraction_manifest,
    validate_extraction_rows,
)


VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
}


def load_manifest(
    manifest_path: Path,
) -> list[dict]:
    return load_extraction_manifest(manifest_path)


def discover_videos(
    root: Path,
) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.suffix.lower()
        in VIDEO_EXTENSIONS
    )


def save_sequence(
    output_path: Path,
    sequence: np.ndarray,
):
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    np.save(
        output_path,
        sequence.astype(
            np.float32
        ),
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "VOXIS batch MediaPipe landmark extraction"
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        help="Root directory containing videos.",
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        help="CSV manifest containing sample_id,video_path,label,signer_id.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "../../data/processed/sign-recognition"
        ),
    )

    parser.add_argument(
        "--output-manifest",
        type=Path,
        help="Destination for the validated sequence manifest (defaults under --output).",
    )

    args = parser.parse_args()

    if not args.input and not args.manifest:
        parser.error(
            "Provide either --input or --manifest."
        )

    if args.manifest:
        rows = load_manifest(
            args.manifest
        )

        records = [
            {
                "video_path": Path(
                    row["video_path"]
                ),
                "label": row["label"],
                "signer_id": row[
                    "signer_id"
                ],
                "sample_id": row["sample_id"],
            }
            for row in rows
        ]

    else:
        videos = discover_videos(
            args.input
        )

        records = [
            {
                "video_path": video,
                "label": video.parent.parent.name.upper(),
                "signer_id": video.parent.name,
                "sample_id": video.stem,
            }
            for video in videos
        ]
        records = validate_extraction_rows(records)

    print(
        f"Videos queued for extraction: {len(records)}"
    )

    success_count = 0
    failed_count = 0
    extracted_rows = []

    with MediaPipeExtractor() as extractor:
        for index, record in enumerate(
            records,
            start=1,
        ):
            try:
                result = extractor.extract_video(
                    record["video_path"]
                )

                output_path = (
                    args.output
                    / record["label"]
                    / record["signer_id"]
                    / f'{record["sample_id"]}.npy'
                )

                save_sequence(
                    output_path,
                    result.frames,
                )

                extracted_rows.append({
                    "sample_id": record["sample_id"],
                    "sequence_path": str(output_path),
                    "label": record["label"].upper(),
                    "signer_id": record["signer_id"],
                    "video_path": str(record["video_path"]),
                })

                success_count += 1

                print(
                    f"[{index}/{len(records)}] "
                    f"OK {record['video_path']} "
                    f"-> {output_path}"
                )

            except Exception as error:
                failed_count += 1

                print(
                    f"[{index}/{len(records)}] "
                    f"FAILED {record['video_path']}: "
                    f"{error}"
                )

    print()
    print("Extraction complete.")
    print(
        f"Successful: {success_count}"
    )
    print(
        f"Failed: {failed_count}"
    )

    output_manifest = args.output_manifest or (args.output / "manifest.csv")
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    with output_manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sample_id", "sequence_path", "label", "signer_id", "video_path"],
        )
        writer.writeheader()
        writer.writerows(extracted_rows)
    print(f"Sequence manifest: {output_manifest}")


if __name__ == "__main__":
    main()

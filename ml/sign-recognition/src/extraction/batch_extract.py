from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from mediapipe_extractor import (
    MediaPipeExtractor,
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
    with manifest_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        return list(
            csv.DictReader(handle)
        )


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
        help="CSV manifest containing video_path,label,signer_id.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "../../data/processed/sign-recognition"
        ),
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
                "sample_id": row[
                    "sample_id"
                ],
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
                "label": video.parent.name.upper(),
                "signer_id": "unknown",
                "sample_id": video.stem,
            }
            for video in videos
        ]

    print(
        f"Videos queued for extraction: {len(records)}"
    )

    success_count = 0
    failed_count = 0

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


if __name__ == "__main__":
    main()

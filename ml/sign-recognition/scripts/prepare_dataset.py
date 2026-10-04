from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from src.preprocessing.augmentation import (
    augment_sequence,
)
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
):
    sequence = np.load(
        source
    ).astype(np.float32)

    sequence = clean_landmarks(
        sequence
    )

    sequence = normalize_landmarks(
        sequence
    )

    if augment:
        sequence = augment_sequence(
            sequence
        )

    sequence = prepare_sequence(
        sequence,
        sequence_length,
    )

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


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Prepare raw extracted landmark arrays."
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
    )

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

    args = parser.parse_args()

    files = sorted(
        args.input.rglob("*.npy")
    )

    if not files:
        raise RuntimeError(
            f"No .npy sequences found under {args.input}"
        )

    for index, source in enumerate(
        files,
        start=1,
    ):
        relative = (
            source.relative_to(
                args.input
            )
        )

        destination = (
            args.output
            / relative
        )

        process_file(
            source,
            destination,
            args.sequence_length,
            args.augment,
        )

        print(
            f"[{index}/{len(files)}] "
            f"prepared {relative}"
        )

    print(
        f"Prepared {len(files)} sequences."
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
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

    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_AUGMENTATION_SEED,
        help="Stable seed used when augmentation is enabled.",
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
            seed=args.seed,
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

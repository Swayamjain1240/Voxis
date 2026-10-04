from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import numpy as np


EXPECTED_FEATURES = 300


def main():
    parser = argparse.ArgumentParser(
        description="Verify VOXIS processed landmark dataset"
    )

    parser.add_argument(
        "--root",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--sequence-length",
        type=int,
        default=60,
    )

    args = parser.parse_args()

    files = sorted(
        args.root.rglob("*.npy")
    )

    if not files:
        raise RuntimeError(
            f"No .npy files found under {args.root}"
        )

    valid = 0
    invalid = 0

    label_counts = Counter()
    signer_counts = Counter()

    for path in files:
        try:
            sequence = np.load(
                path
            )

            if sequence.shape != (
                args.sequence_length,
                EXPECTED_FEATURES,
            ):
                raise ValueError(
                    f"shape={sequence.shape}"
                )

            label = path.parent.parent.name
            signer = path.parent.name

            label_counts[label] += 1
            signer_counts[signer] += 1

            valid += 1

        except Exception as error:
            invalid += 1
            print(
                f"INVALID: {path} -> {error}"
            )

    print()
    print(
        "================ DATASET REPORT ================"
    )
    print(
        f"Total files : {len(files)}"
    )
    print(
        f"Valid       : {valid}"
    )
    print(
        f"Invalid     : {invalid}"
    )
    print()
    print(
        "Labels:"
    )

    for label, count in sorted(
        label_counts.items()
    ):
        print(
            f"  {label}: {count}"
        )

    print()
    print(
        "Signers:"
    )

    for signer, count in sorted(
        signer_counts.items()
    ):
        print(
            f"  {signer}: {count}"
        )


if __name__ == "__main__":
    main()

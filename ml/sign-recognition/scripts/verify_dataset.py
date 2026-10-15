from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import numpy as np

from src.contracts.label_map import load_label_map
from src.contracts.sign_input import FEATURES_PER_FRAME, SEQUENCE_LENGTH, validate_sequence


EXPECTED_FEATURES = FEATURES_PER_FRAME


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
        default=SEQUENCE_LENGTH,
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
    label_map = load_label_map()

    for path in files:
        try:
            sequence = np.load(
                path,
                allow_pickle=False,
            )

            validate_sequence(
                sequence,
                sequence_length=args.sequence_length,
                features_per_frame=EXPECTED_FEATURES,
            )

            label = path.parent.parent.name
            signer = path.parent.name

            if label.upper() not in label_map.gloss_to_label:
                raise ValueError(f"unknown canonical label={label}")
            if not signer or signer.casefold() == "unknown":
                raise ValueError("known signer_id is required")

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

    if invalid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

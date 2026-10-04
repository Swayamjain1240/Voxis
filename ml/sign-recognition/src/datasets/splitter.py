from __future__ import annotations

from collections import defaultdict


def signer_wise_split(
    rows: list[dict],
    train_ratio: float = 0.70,
    validation_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> dict[str, list[dict]]:

    total_ratio = (
        train_ratio
        + validation_ratio
        + test_ratio
    )

    if abs(total_ratio - 1.0) > 1e-6:
        raise ValueError(
            "Train/validation/test ratios must sum to 1."
        )

    by_signer = defaultdict(list)

    for row in rows:
        signer = str(
            row["signer_id"]
        )

        if signer.lower() == "unknown":
            raise ValueError(
                "Signer-wise split requires valid signer_id."
            )

        by_signer[signer].append(row)

    signers = sorted(
        by_signer.keys()
    )

    if len(signers) < 3:
        raise ValueError(
            "At least 3 signers are required for "
            "train/validation/test split."
        )

    train_count = max(
        1,
        round(
            len(signers)
            * train_ratio
        ),
    )

    validation_count = max(
        1,
        round(
            len(signers)
            * validation_ratio
        ),
    )

    if (
        train_count
        + validation_count
        >= len(signers)
    ):
        validation_count = 1
        train_count = len(signers) - 2

    train_signers = signers[
        :train_count
    ]

    validation_signers = signers[
        train_count:
        train_count + validation_count
    ]

    test_signers = signers[
        train_count + validation_count:
    ]

    def collect(
        selected_signers
    ):
        return [
            row
            for signer in selected_signers
            for row in by_signer[
                signer
            ]
        ]

    return {
        "train": collect(
            train_signers
        ),
        "validation": collect(
            validation_signers
        ),
        "test": collect(
            test_signers
        ),
        "train_signers": train_signers,
        "validation_signers":
            validation_signers,
        "test_signers": test_signers,
    }

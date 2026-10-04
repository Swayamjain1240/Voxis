from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def build_confusion_matrix(
    predictions,
    targets,
    num_classes: int,
):
    matrix = np.zeros(
        (
            num_classes,
            num_classes,
        ),
        dtype=np.int64,
    )

    for target, prediction in zip(
        targets,
        predictions,
    ):
        matrix[
            int(target),
            int(prediction),
        ] += 1

    return matrix


def save_confusion_matrix(
    matrix: np.ndarray,
    labels: list[str],
    output_path: str | Path,
):
    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "labels": labels,
        "matrix": matrix.tolist(),
    }

    output_path.write_text(
        json.dumps(
            payload,
            indent=2,
        ),
        encoding="utf-8",
    )

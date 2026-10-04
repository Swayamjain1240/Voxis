from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

from src.datasets.dataset import (
    SignSequenceDataset,
)
from src.evaluation.confusion_matrix import (
    build_confusion_matrix,
    save_confusion_matrix,
)
from src.evaluation.metrics import (
    accuracy,
    top_k_accuracy,
)
from src.models.transformer import (
    SignTransformer,
)


def load_manifest(path):
    import csv

    with Path(path).open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        return list(
            csv.DictReader(handle)
        )


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate VOXIS sign model"
    )

    parser.add_argument(
        "--checkpoint",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "artifacts/reports/evaluation.json"
        ),
    )

    parser.add_argument(
        "--device",
        default=(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        ),
    )

    args = parser.parse_args()

    checkpoint = torch.load(
        args.checkpoint,
        map_location=args.device,
        weights_only=False,
    )

    label_map = checkpoint[
        "label_map"
    ]

    rows = load_manifest(
        args.manifest
    )

    from src.datasets.splitter import (
        signer_wise_split,
    )

    split = signer_wise_split(
        rows
    )

    dataset = SignSequenceDataset(
        split["test"],
        label_map,
    )

    loader = DataLoader(
        dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0,
    )

    model = SignTransformer(
        input_features=checkpoint[
            "input_features"
        ],
        num_classes=len(
            label_map
        ),
    )

    model.load_state_dict(
        checkpoint[
            "model_state_dict"
        ]
    )

    model.to(
        args.device
    )

    model.eval()

    predictions = []
    targets = []
    probabilities = []

    with torch.no_grad():
        for inputs, batch_targets in loader:
            inputs = inputs.to(
                args.device
            )

            logits = model(
                inputs
            )

            probs = torch.softmax(
                logits,
                dim=-1,
            )

            batch_predictions = (
                probs.argmax(
                    dim=-1
                )
                .cpu()
                .numpy()
            )

            predictions.extend(
                batch_predictions.tolist()
            )

            targets.extend(
                batch_targets.numpy().tolist()
            )

            probabilities.extend(
                probs.cpu().numpy().tolist()
            )

    inverse_map = {
        index: label
        for label, index
        in label_map.items()
    }

    labels = [
        inverse_map[index]
        for index in range(
            len(label_map)
        )
    ]

    matrix = (
        build_confusion_matrix(
            predictions,
            targets,
            len(label_map),
        )
    )

    report = {
        "accuracy": accuracy(
            predictions,
            targets,
        ),
        "top_3_accuracy":
            top_k_accuracy(
                probabilities,
                targets,
                k=3,
            ),
        "test_signers":
            split["test_signers"],
        "labels": labels,
        "num_test_samples":
            len(targets),
        "confusion_matrix":
            matrix.tolist(),
    }

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    save_confusion_matrix(
        matrix,
        labels,
        args.output.with_name(
            "confusion_matrix.json"
        ),
    )

    print(
        json.dumps(
            report,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

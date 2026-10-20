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
from src.datasets.manifest import load_manifest as load_validated_manifest
from src.evaluation.confusion_matrix import (
    save_confusion_matrix,
)
from src.evaluation.benchmark import compare_to_baseline
from src.evaluation.report import build_evaluation_report
from src.models.baseline import TemporalCentroidClassifier
from src.contracts.model_config import model_config_from_mapping
from src.models.factory import create_model
from src.contracts.model_metadata import validate_checkpoint_metadata


def load_manifest(path):
    return load_validated_manifest(path)


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

    metadata = validate_checkpoint_metadata(checkpoint)

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
    train_dataset = SignSequenceDataset(
        split["train"],
        label_map,
    )

    loader = DataLoader(
        dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0,
    )

    model_config = model_config_from_mapping(
        checkpoint.get("model_config", {
            "model_version": metadata.model_version,
            "num_classes": len(label_map),
        })
    )
    model = create_model(model_config)

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

    report = build_evaluation_report(
        predictions,
        targets,
        probabilities,
        labels=labels,
        signer_ids=[row["signer_id"] for row in split["test"]],
        test_signers=split["test_signers"],
        metadata=metadata.as_dict(),
    )

    baseline = TemporalCentroidClassifier(num_classes=len(label_map))
    train_sequences = np.stack([
        train_dataset._load_sequence(row["sequence_path"])
        for row in split["train"]
    ])
    train_targets = [label_map[row["label"].upper()] for row in split["train"]]
    baseline.fit(train_sequences, train_targets)
    baseline_probabilities = baseline.predict_proba([
        dataset._load_sequence(row["sequence_path"])
        for row in split["test"]
    ])
    baseline_report = build_evaluation_report(
        baseline.predict([
            dataset._load_sequence(row["sequence_path"])
            for row in split["test"]
        ]),
        targets,
        baseline_probabilities,
        labels=labels,
        signer_ids=[row["signer_id"] for row in split["test"]],
        test_signers=split["test_signers"],
        metadata={
            "model_version": "temporal-centroid-baseline",
            "vocabulary_version": metadata.vocabulary_version,
            "preprocessing_version": metadata.preprocessing_version,
        },
    )
    report["baseline"] = baseline_report
    report["baseline_comparison"] = compare_to_baseline(report, baseline_report)

    matrix = np.asarray(report["confusion_matrix"], dtype=np.int64)

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

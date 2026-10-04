from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

from src.datasets.dataset import (
    SignSequenceDataset,
)
from src.datasets.splitter import (
    signer_wise_split,
)
from src.models.transformer import (
    SignTransformer,
)
from src.training.trainer import (
    SignTrainer,
)


def seed_everything(
    seed: int,
):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(
            seed
        )


def load_manifest(
    path: Path,
):
    import csv

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        return list(
            csv.DictReader(handle)
        )


def build_label_map(
    rows: list[dict],
):
    labels = sorted(
        {
            row["label"].upper()
            for row in rows
        }
    )

    return {
        label: index
        for index, label in enumerate(
            labels
        )
    }


def main():
    parser = argparse.ArgumentParser(
        description="VOXIS sign model training"
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
            "artifacts/checkpoints"
        ),
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
    )

    parser.add_argument(
        "--lr",
        type=float,
        default=3e-4,
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

    seed_everything(42)

    rows = load_manifest(
        args.manifest
    )

    if not rows:
        raise RuntimeError(
            "Manifest is empty."
        )

    label_map = build_label_map(
        rows
    )

    split = signer_wise_split(
        rows
    )

    train_dataset = SignSequenceDataset(
        split["train"],
        label_map,
    )

    validation_dataset = SignSequenceDataset(
        split["validation"],
        label_map,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=0,
        pin_memory=(
            args.device.startswith("cuda")
        ),
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=(
            args.device.startswith("cuda")
        ),
    )

    model = SignTransformer(
        input_features=300,
        num_classes=len(
            label_map
        ),
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=1e-4,
    )

    criterion = nn.CrossEntropyLoss(
        label_smoothing=0.05
    )

    trainer = SignTrainer(
        model=model,
        optimizer=optimizer,
        criterion=criterion,
        device=args.device,
    )

    args.output.mkdir(
        parents=True,
        exist_ok=True,
    )

    best_accuracy = -1.0

    for epoch in range(
        1,
        args.epochs + 1,
    ):
        train_result = (
            trainer.train_epoch(
                train_loader
            )
        )

        validation_result = (
            trainer.evaluate(
                validation_loader
            )
        )

        print(
            f"Epoch {epoch:03d} | "
            f"train_loss={train_result.loss:.4f} | "
            f"train_acc={train_result.accuracy:.4f} | "
            f"val_loss={validation_result.loss:.4f} | "
            f"val_acc={validation_result.accuracy:.4f}"
        )

        if (
            validation_result.accuracy
            > best_accuracy
        ):
            best_accuracy = (
                validation_result.accuracy
            )

            checkpoint = {
                "epoch": epoch,
                "model_state_dict":
                    model.state_dict(),
                "optimizer_state_dict":
                    optimizer.state_dict(),
                "label_map": label_map,
                "input_features": 300,
                "sequence_length": 60,
                "validation_accuracy":
                    best_accuracy,
            }

            checkpoint_path = (
                args.output
                / "best_transformer.pt"
            )

            torch.save(
                checkpoint,
                checkpoint_path,
            )

            print(
                f"Saved checkpoint: "
                f"{checkpoint_path}"
            )

    split_metadata = {
        "train_signers":
            split["train_signers"],
        "validation_signers":
            split["validation_signers"],
        "test_signers":
            split["test_signers"],
        "label_map": label_map,
    }

    metadata_path = (
        args.output
        / "split_metadata.json"
    )

    metadata_path.write_text(
        json.dumps(
            split_metadata,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

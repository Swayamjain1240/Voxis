from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from src.models.transformer import (
    SignTransformer,
)


def main():
    parser = argparse.ArgumentParser(
        description="Export VOXIS sign model to ONNX"
    )

    parser.add_argument(
        "--checkpoint",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "artifacts/onnx/sign_transformer.onnx"
        ),
    )

    parser.add_argument(
        "--opset",
        type=int,
        default=17,
    )

    args = parser.parse_args()

    checkpoint = torch.load(
        args.checkpoint,
        map_location="cpu",
        weights_only=False,
    )

    model = SignTransformer(
        input_features=checkpoint[
            "input_features"
        ],
        num_classes=len(
            checkpoint["label_map"]
        ),
    )

    model.load_state_dict(
        checkpoint[
            "model_state_dict"
        ]
    )

    model.eval()

    dummy_input = torch.randn(
        1,
        checkpoint.get(
            "sequence_length",
            60,
        ),
        checkpoint[
            "input_features"
        ],
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    torch.onnx.export(
        model,
        dummy_input,
        str(args.output),
        input_names=[
            "landmark_sequence"
        ],
        output_names=[
            "logits"
        ],
        dynamic_axes={
            "landmark_sequence": {
                0: "batch"
            },
            "logits": {
                0: "batch"
            },
        },
        opset_version=args.opset,
    )

    label_map_path = (
        args.output.parent
        / "label_map.json"
    )

    label_map_path.write_text(
        json.dumps(
            checkpoint[
                "label_map"
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"ONNX model exported to: "
        f"{args.output}"
    )


if __name__ == "__main__":
    main()

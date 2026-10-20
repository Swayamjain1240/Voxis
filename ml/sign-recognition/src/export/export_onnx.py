from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from src.contracts.model_metadata import validate_checkpoint_metadata
from src.contracts.label_map import load_label_map
from src.contracts.model_config import model_config_from_mapping
from src.models.factory import create_model


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

    metadata = validate_checkpoint_metadata(checkpoint)

    model_config = model_config_from_mapping(
        checkpoint.get("model_config", {
            "model_version": metadata.model_version,
            "num_classes": len(checkpoint["label_map"]),
        })
    )
    model = create_model(model_config)

    model.load_state_dict(
        checkpoint[
            "model_state_dict"
        ]
    )

    model.eval()

    dummy_input = torch.randn(
        1,
            metadata.sequence_length,
            metadata.input_features,
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
        json.dumps(load_label_map().as_dict(), indent=2),
        encoding="utf-8",
    )

    (args.output.parent / "model_metadata.json").write_text(
        json.dumps(metadata.as_dict(), indent=2),
        encoding="utf-8",
    )

    print(
        f"ONNX model exported to: "
        f"{args.output}"
    )


if __name__ == "__main__":
    main()

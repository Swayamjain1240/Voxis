import torch

from src.models.transformer import (
    SignTransformer,
)

from src.models.conformer import (
    SignConformer,
)


def test_transformer_shape():
    model = SignTransformer(
        input_features=300,
        num_classes=12,
    )

    inputs = torch.randn(
        2,
        60,
        300,
    )

    outputs = model(
        inputs
    )

    assert outputs.shape == (
        2,
        12,
    )


def test_conformer_shape():
    model = SignConformer(
        input_features=300,
        num_classes=12,
    )

    inputs = torch.randn(
        2,
        60,
        300,
    )

    outputs = model(
        inputs
    )

    assert outputs.shape == (
        2,
        12,
    )

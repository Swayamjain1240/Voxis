from __future__ import annotations

from src.contracts.model_config import ModelConfig
from src.models.conformer import SignConformer
from src.models.transformer import SignTransformer


def create_model(config: ModelConfig):
    config.validate()
    model_class = SignConformer if config.architecture == "conformer" else SignTransformer
    kwargs = {
        "input_features": config.input_features,
        "num_classes": config.num_classes,
        "d_model": config.d_model,
        "num_heads": config.num_heads,
        "num_layers": config.num_layers,
        "feedforward_dim": config.feedforward_dim,
        "dropout": config.dropout,
    }
    return model_class(**kwargs)

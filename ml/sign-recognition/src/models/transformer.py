from __future__ import annotations

import math

import torch
from torch import nn


class SinusoidalPositionalEncoding(
    nn.Module
):
    def __init__(
        self,
        d_model: int,
        max_length: int = 512,
    ):
        super().__init__()

        encoding = torch.zeros(
            max_length,
            d_model,
        )

        position = torch.arange(
            max_length,
            dtype=torch.float32,
        ).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(
                0,
                d_model,
                2,
                dtype=torch.float32,
            )
            * (
                -math.log(10000.0)
                / d_model
            )
        )

        encoding[
            :,
            0::2,
        ] = torch.sin(
            position
            * div_term
        )

        encoding[
            :,
            1::2,
        ] = torch.cos(
            position
            * div_term
        )

        self.register_buffer(
            "encoding",
            encoding.unsqueeze(0),
        )

    def forward(self, x):
        sequence_length = x.size(1)

        return (
            x
            + self.encoding[
                :,
                :sequence_length,
                :,
            ]
        )


class SignTransformer(
    nn.Module
):
    def __init__(
        self,
        input_features: int,
        num_classes: int,
        d_model: int = 256,
        num_heads: int = 8,
        num_layers: int = 4,
        feedforward_dim: int = 1024,
        dropout: float = 0.10,
    ):
        super().__init__()

        if d_model % num_heads != 0:
            raise ValueError(
                "d_model must be divisible by num_heads."
            )

        self.input_projection = nn.Sequential(
            nn.LayerNorm(
                input_features
            ),
            nn.Linear(
                input_features,
                d_model,
            ),
        )

        self.position = (
            SinusoidalPositionalEncoding(
                d_model
            )
        )

        encoder_layer = (
            nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=num_heads,
                dim_feedforward=feedforward_dim,
                dropout=dropout,
                activation="gelu",
                batch_first=True,
                norm_first=True,
            )
        )

        self.encoder = (
            nn.TransformerEncoder(
                encoder_layer,
                num_layers=num_layers,
            )
        )

        self.norm = nn.LayerNorm(
            d_model
        )

        self.classifier = nn.Linear(
            d_model,
            num_classes,
        )

    def forward(
        self,
        x,
    ):
        """
        x:
            [batch, sequence, features]
        """

        x = self.input_projection(x)
        x = self.position(x)
        x = self.encoder(x)
        x = self.norm(x)

        pooled = x.mean(
            dim=1
        )

        return self.classifier(
            pooled
        )

from __future__ import annotations

import torch
from torch import nn


class ConformerBlock(
    nn.Module
):
    def __init__(
        self,
        d_model: int = 256,
        num_heads: int = 8,
        feedforward_dim: int = 1024,
        conv_kernel_size: int = 5,
        dropout: float = 0.10,
    ):
        super().__init__()

        self.ffn1 = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(
                d_model,
                feedforward_dim,
            ),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(
                feedforward_dim,
                d_model,
            ),
            nn.Dropout(dropout),
        )

        self.attention_norm = (
            nn.LayerNorm(d_model)
        )

        self.attention = (
            nn.MultiheadAttention(
                embed_dim=d_model,
                num_heads=num_heads,
                dropout=dropout,
                batch_first=True,
            )
        )

        self.conv_norm = (
            nn.LayerNorm(d_model)
        )

        self.depthwise_conv = (
            nn.Conv1d(
                d_model,
                d_model,
                kernel_size=conv_kernel_size,
                padding=conv_kernel_size // 2,
                groups=d_model,
            )
        )

        self.pointwise_conv = (
            nn.Conv1d(
                d_model,
                d_model,
                kernel_size=1,
            )
        )

        self.activation = nn.GELU()

        self.ffn2 = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(
                d_model,
                feedforward_dim,
            ),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(
                feedforward_dim,
                d_model,
            ),
            nn.Dropout(dropout),
        )

        self.final_norm = (
            nn.LayerNorm(d_model)
        )

    def forward(self, x):
        x = x + 0.5 * self.ffn1(x)

        attention_input = (
            self.attention_norm(x)
        )

        attended, _ = (
            self.attention(
                attention_input,
                attention_input,
                attention_input,
                need_weights=False,
            )
        )

        x = x + attended

        conv_input = self.conv_norm(x)

        conv = (
            conv_input.transpose(
                1,
                2,
            )
        )

        conv = (
            self.depthwise_conv(conv)
        )

        conv = self.activation(
            conv
        )

        conv = (
            self.pointwise_conv(conv)
        )

        x = x + conv.transpose(
            1,
            2,
        )

        x = x + 0.5 * self.ffn2(x)

        return self.final_norm(x)


class SignConformer(
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
        conv_kernel_size: int = 5,
    ):
        super().__init__()

        self.input_projection = nn.Sequential(
            nn.LayerNorm(
                input_features
            ),
            nn.Linear(
                input_features,
                d_model,
            ),
        )

        self.blocks = nn.ModuleList(
            [
                ConformerBlock(
                    d_model=d_model,
                    num_heads=num_heads,
                    feedforward_dim=feedforward_dim,
                    conv_kernel_size=conv_kernel_size,
                    dropout=dropout,
                )
                for _ in range(
                    num_layers
                )
            ]
        )

        self.classifier = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(
                d_model,
                num_classes,
            ),
        )

    def forward(
        self,
        x,
    ):
        x = self.input_projection(x)

        for block in self.blocks:
            x = block(x)

        pooled = x.mean(
            dim=1
        )

        return self.classifier(
            pooled
        )

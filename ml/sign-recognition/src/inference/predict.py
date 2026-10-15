from __future__ import annotations

import numpy as np
import torch

from src.contracts.label_map import load_label_map
from src.contracts.sign_input import validate_sequence, validate_top_k


class SignPredictor:
    def __init__(
        self,
        model,
        label_map: dict[str, int],
        device: str = "cpu",
        model_version: str = "unversioned",
        preprocessing_version: str = "1.0.0",
    ):
        canonical = load_label_map()
        if label_map != canonical.gloss_to_label:
            raise ValueError("Predictor label map must match the shared vocabulary map.")
        self.model = model.to(
            device
        )

        self.device = torch.device(
            device
        )

        self.index_to_label = {
            index: label
            for label, index
            in label_map.items()
        }
        self.model_version = model_version
        self.preprocessing_version = preprocessing_version
        self.vocabulary_version = canonical.version

        self.model.eval()

    @torch.no_grad()
    def predict(
        self,
        sequence: np.ndarray,
        top_k: int = 3,
    ):
        array = validate_sequence(sequence)
        top_k = validate_top_k(top_k)

        tensor = torch.from_numpy(
            array
        ).unsqueeze(0).to(
            self.device
        )

        logits = self.model(
            tensor
        )

        probabilities = (
            torch.softmax(
                logits,
                dim=-1,
            )[0]
        )

        k = min(
            top_k,
            probabilities.numel(),
        )

        values, indices = (
            torch.topk(
                probabilities,
                k=k,
            )
        )

        return [
            {
                "gloss":
                    self.index_to_label[
                        int(index)
                    ],
                "label": int(index),
                "confidence":
                    float(value),
                "model_version": self.model_version,
                "vocabulary_version": self.vocabulary_version,
                "preprocessing_version": self.preprocessing_version,
            }
            for value, index in zip(
                values.cpu(),
                indices.cpu(),
            )
        ]

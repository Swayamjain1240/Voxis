from __future__ import annotations

import numpy as np
import torch


class SignPredictor:
    def __init__(
        self,
        model,
        label_map: dict[str, int],
        device: str = "cpu",
    ):
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

        self.model.eval()

    @torch.no_grad()
    def predict(
        self,
        sequence: np.ndarray,
        top_k: int = 3,
    ):
        array = np.asarray(
            sequence,
            dtype=np.float32,
        )

        if array.ndim != 2:
            raise ValueError(
                "Expected sequence [frames, features]."
            )

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
                "confidence":
                    float(value),
            }
            for value, index in zip(
                values.cpu(),
                indices.cpu(),
            )
        ]

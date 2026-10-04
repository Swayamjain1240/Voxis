from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset


class SignSequenceDataset(Dataset):
    """
    Dataset layout:

    processed_root/
        PAIN/
            signer_01/
                sample_001.npy
        HELP/
            signer_02/
                sample_002.npy

    The manifest may also be used to provide explicit paths/labels.
    """

    def __init__(
        self,
        samples: list[dict],
        label_map: dict[str, int],
        sequence_length: int = 60,
    ):
        self.samples = samples
        self.label_map = label_map
        self.sequence_length = sequence_length

    def __len__(self):
        return len(self.samples)

    def _load_sequence(
        self,
        path: str | Path,
    ) -> np.ndarray:
        sequence = np.load(
            path
        ).astype(np.float32)

        if sequence.ndim != 2:
            raise ValueError(
                f"{path} must contain [frames, features]."
            )

        if len(sequence) != self.sequence_length:
            raise ValueError(
                f"{path} has {len(sequence)} frames; "
                f"expected {self.sequence_length}."
            )

        return sequence

    def __getitem__(
        self,
        index: int,
    ):
        sample = self.samples[index]

        sequence = self._load_sequence(
            sample["sequence_path"]
        )

        label = sample["label"].upper()

        if label not in self.label_map:
            raise KeyError(
                f"Unknown label: {label}"
            )

        return (
            torch.from_numpy(sequence),
            torch.tensor(
                self.label_map[label],
                dtype=torch.long,
            ),
        )

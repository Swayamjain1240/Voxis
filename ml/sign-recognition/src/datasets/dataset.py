from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset

from src.contracts.sign_input import validate_sequence


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

        try:
            return validate_sequence(
                sequence,
                sequence_length=self.sequence_length,
            )
        except ValueError as error:
            raise ValueError(f"Invalid sequence at {path}: {error}") from error

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

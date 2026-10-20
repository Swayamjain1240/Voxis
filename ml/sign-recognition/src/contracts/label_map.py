from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


SCHEMA_VERSION = "1.0.0"


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


@dataclass(frozen=True)
class CanonicalLabelMap:
    version: str
    gloss_to_label: dict[str, int]
    label_to_gloss: dict[int, str]
    unknown_label: int

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(
            self.label_to_gloss[index]
            for index in sorted(self.label_to_gloss)
        )

    def as_dict(self) -> dict[str, object]:
        """Return the shared contract used by exported model sidecars."""
        return {
            "version": self.version,
            "labels": {
                str(index): gloss
                for index, gloss in self.label_to_gloss.items()
            },
            "gloss_to_label": dict(self.gloss_to_label),
            "unknown_label": self.unknown_label,
        }

    def validate_rows(self, rows: list[Mapping[str, str]]) -> None:
        for row in rows:
            gloss = str(row.get("label", "")).strip().upper()
            if gloss not in self.gloss_to_label:
                raise ValueError(
                    f"Manifest label {gloss!r} is not in the canonical vocabulary."
                )


def load_label_map(
    path: str | Path | None = None,
    vocabulary_path: str | Path | None = None,
) -> CanonicalLabelMap:
    label_path = Path(path) if path else (
        _repository_root() / "shared" / "vocabulary" / "label_map.json"
    )
    vocabulary_file = Path(vocabulary_path) if vocabulary_path else (
        _repository_root() / "shared" / "vocabulary" / "vocabulary.json"
    )

    with label_path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    with vocabulary_file.open("r", encoding="utf-8-sig") as handle:
        vocabulary = json.load(handle)

    if payload.get("version") != SCHEMA_VERSION:
        raise ValueError("Label-map version is not supported.")
    if vocabulary.get("version") != SCHEMA_VERSION:
        raise ValueError("Vocabulary and label-map versions do not match.")

    vocabulary_glosses = tuple(item["gloss"] for item in vocabulary.get("items", []))
    raw_labels = payload.get("labels")
    raw_gloss_to_label = payload.get("gloss_to_label")
    unknown_label = payload.get("unknown_label")
    if not isinstance(raw_labels, dict) or not isinstance(raw_gloss_to_label, dict):
        raise ValueError("Label-map labels and reverse mapping are required.")
    if unknown_label != -1:
        raise ValueError("The canonical unknown label must be -1.")

    try:
        label_to_gloss = {int(index): str(gloss) for index, gloss in raw_labels.items()}
        gloss_to_label = {
            str(gloss): int(index)
            for gloss, index in raw_gloss_to_label.items()
        }
    except (TypeError, ValueError) as error:
        raise ValueError("Label-map indices must be integers.") from error

    expected_indices = set(range(len(vocabulary_glosses)))
    if set(label_to_gloss) != expected_indices:
        raise ValueError("Label-map indices must be contiguous and match vocabulary size.")
    if tuple(label_to_gloss[index] for index in sorted(label_to_gloss)) != vocabulary_glosses:
        raise ValueError("Label-map order must match the shared vocabulary order.")
    if {
        gloss: label_to_gloss[index]
        for gloss, index in gloss_to_label.items()
    } != {gloss: gloss for gloss in vocabulary_glosses}:
        raise ValueError("Label-map reverse mappings do not agree.")

    return CanonicalLabelMap(
        version=payload["version"],
        gloss_to_label=gloss_to_label,
        label_to_gloss=label_to_gloss,
        unknown_label=unknown_label,
    )

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping

from src.contracts.label_map import load_label_map


CONTRACT_FILES = ("vocabulary.json", "label_map.json", "contexts.json")


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def load_freeze(path: str | Path | None = None) -> dict[str, object]:
    freeze_path = Path(path) if path else repository_root() / "shared" / "vocabulary" / "freeze.json"
    payload = json.loads(freeze_path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("Vocabulary freeze must be an object.")
    return payload


def verify_vocabulary_freeze(
    freeze: Mapping[str, object] | None = None,
    *,
    root: str | Path | None = None,
) -> dict[str, str]:
    payload = freeze or load_freeze()
    if payload.get("schema_version") != "1.0.0":
        raise ValueError("Vocabulary freeze schema version is not supported.")
    if payload.get("status") != "frozen":
        raise ValueError("Shared vocabulary is not marked frozen.")

    shared_root = Path(root) if root else repository_root() / "shared" / "vocabulary"
    contracts = payload.get("contracts")
    if not isinstance(contracts, Mapping):
        raise ValueError("Vocabulary freeze must list contract hashes.")

    observed: dict[str, str] = {}
    for filename in CONTRACT_FILES:
        path = shared_root / filename
        if not path.exists():
            raise ValueError(f"Frozen vocabulary contract is missing: {filename}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = contracts.get(filename)
        if expected != f"sha256:{digest}":
            raise ValueError(f"Frozen vocabulary contract changed: {filename}")
        observed[filename] = digest

    label_map = load_label_map(shared_root / "label_map.json", shared_root / "vocabulary.json")
    if payload.get("vocabulary_version") != label_map.version:
        raise ValueError("Frozen vocabulary version does not match the label map.")
    return observed

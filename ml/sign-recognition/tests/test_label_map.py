import json

import pytest

from src.contracts.label_map import load_label_map


def test_load_label_map_preserves_shared_order():
    label_map = load_label_map()

    assert label_map.version == "1.0.0"
    assert label_map.labels[:4] == ("DOCTOR", "PATIENT", "MEDICINE", "SICK")
    assert label_map.gloss_to_label["PAIN"] == 11
    assert label_map.unknown_label == -1


def test_manifest_labels_must_use_shared_vocabulary():
    label_map = load_label_map()

    label_map.validate_rows([{"label": "pain"}])
    with pytest.raises(ValueError, match="canonical vocabulary"):
        label_map.validate_rows([{"label": "FEVER"}])


def test_invalid_label_map_order_is_rejected(tmp_path):
    canonical_path = tmp_path / "label_map.json"
    vocabulary_path = tmp_path / "vocabulary.json"
    canonical_path.write_text(
        json.dumps({
            "version": "1.0.0",
            "labels": {"0": "PATIENT"},
            "gloss_to_label": {"PATIENT": 0},
            "unknown_label": -1,
        }),
        encoding="utf-8",
    )
    vocabulary_path.write_text(
        json.dumps({"version": "1.0.0", "items": [{"gloss": "DOCTOR"}]}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="order"):
        load_label_map(canonical_path, vocabulary_path)

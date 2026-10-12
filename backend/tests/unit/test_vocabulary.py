import json

import pytest

from app.services.language.text_to_gloss import text_to_gloss
from app.services.language.vocabulary import load_vocabulary


def test_loader_reads_items_and_context_allowlists(tmp_path):
    vocabulary_path = tmp_path / "vocabulary.json"
    contexts_path = tmp_path / "contexts.json"
    vocabulary_path.write_text(
        json.dumps(
            {
                "version": "test-1",
                "items": [
                    {"gloss": "HELLO", "text": "hello", "contexts": ["general"]},
                    {"gloss": "MONEY", "text": "money", "contexts": ["bank"]},
                ],
            }
        ),
        encoding="utf-8",
    )
    contexts_path.write_text(
        json.dumps(
            {
                "version": "test-1",
                "contexts": {
                    "general": {"allowed_glosses": ["HELLO"]},
                    "bank": {"allowed_glosses": ["MONEY"]},
                },
            }
        ),
        encoding="utf-8",
    )

    vocabulary = load_vocabulary(vocabulary_path, contexts_path)

    assert vocabulary.version == "test-1"
    assert vocabulary.glosses == {"HELLO", "MONEY"}
    assert vocabulary.keywords["hello"] == "HELLO"
    assert vocabulary.contexts["bank"] == {"MONEY"}
    assert vocabulary.default_context is None


def test_context_file_is_optional(tmp_path):
    vocabulary_path = tmp_path / "vocabulary.json"
    vocabulary_path.write_text(
        json.dumps(
            {
                "version": "test-1",
                "items": [{"gloss": "HELLO", "text": "hello"}],
            }
        ),
        encoding="utf-8",
    )

    vocabulary = load_vocabulary(
        vocabulary_path,
        tmp_path / "missing-contexts.json",
    )

    assert vocabulary.glosses == {"HELLO"}


def test_text_to_gloss_uses_loaded_vocabulary_without_hardcoded_labels(tmp_path):
    vocabulary_path = tmp_path / "vocabulary.json"
    vocabulary_path.write_text(
        json.dumps(
            {
                "version": "test-1",
                "items": [
                    {"gloss": "HELLO", "text": "hello"},
                ],
            }
        ),
        encoding="utf-8",
    )
    vocabulary = load_vocabulary(vocabulary_path)

    assert text_to_gloss(
        "hello doctor",
        vocabulary=vocabulary,
    ) == ["HELLO"]


def test_text_to_gloss_applies_context_allowlist():
    assert text_to_gloss(
        "doctor money",
        context="bank",
    ) == ["MONEY"]


def test_text_to_gloss_rejects_unknown_context():
    with pytest.raises(Exception) as error:
        text_to_gloss("help", context="unknown")

    assert error.value.status_code == 400

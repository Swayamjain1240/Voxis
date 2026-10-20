import pytest

from src.contracts.avatar_coverage import audit_avatar_coverage
from src.contracts.vocabulary_freeze import verify_vocabulary_freeze


def test_shared_vocabulary_freeze_matches_all_contract_digests():
    observed = verify_vocabulary_freeze()
    assert set(observed) == {"vocabulary.json", "label_map.json", "contexts.json"}


def test_changed_contract_is_rejected(tmp_path):
    freeze = {
        "schema_version": "1.0.0",
        "status": "frozen",
        "vocabulary_version": "1.0.0",
        "contracts": {
            "vocabulary.json": "sha256:bad",
            "label_map.json": "sha256:bad",
            "contexts.json": "sha256:bad",
        },
    }
    shared = tmp_path / "shared"
    shared.mkdir()
    for filename in ("vocabulary.json", "label_map.json", "contexts.json"):
        (shared / filename).write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="changed"):
        verify_vocabulary_freeze(freeze, root=shared)


def test_avatar_coverage_reports_missing_and_unexpected_glosses():
    coverage = audit_avatar_coverage(["PAIN", "not-a-sign"])
    assert coverage["supported"] == ["PAIN"]
    assert "DOCTOR" in coverage["missing"]
    assert coverage["unexpected"] == ["NOT-A-SIGN"]

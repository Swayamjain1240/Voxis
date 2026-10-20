from app.services.language.gloss_conversion import (
    convert_text_to_gloss,
    validate_gloss_tokens,
)


def test_gloss_validation_separates_unsupported_and_deduplicates():
    accepted, unsupported = validate_gloss_tokens(["pain", "PAIN", "FEVER"])
    assert accepted == ["PAIN"]
    assert unsupported == ["FEVER"]


def test_generator_output_is_constrained_to_shared_vocabulary():
    result = convert_text_to_gloss(
        "ignored",
        generator=lambda _text, _context: {"glosses": ["WHERE", "PAIN", "FEVER"]},
    )
    assert result.glosses == ["WHERE", "PAIN"]
    assert result.unsupported == ["FEVER"]
    assert result.source == "llm"


def test_generator_failure_uses_deterministic_fallback():
    result = convert_text_to_gloss(
        "Where does it hurt?",
        generator=lambda _text, _context: (_ for _ in ()).throw(RuntimeError("offline")),
    )
    assert result.glosses == ["WHERE", "PAIN"]
    assert result.source == "deterministic_fallback"

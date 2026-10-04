from app.services.language.gloss_to_text import (
    gloss_to_text,
)

from app.services.language.text_to_gloss import (
    text_to_gloss,
)


def test_text_to_gloss():
    result = text_to_gloss(
        "Where is the pain?"
    )

    assert "WHERE" in result
    assert "PAIN" in result


def test_text_to_gloss_only_known_tokens():
    result = text_to_gloss(
        "I have an elephant"
    )

    assert result == []


def test_gloss_to_text():
    result = gloss_to_text(
        [
            "WHERE",
            "PAIN",
        ]
    )

    assert result == (
        "Where is the pain?"
    )


def test_gloss_to_text_empty():
    assert gloss_to_text([]) == ""

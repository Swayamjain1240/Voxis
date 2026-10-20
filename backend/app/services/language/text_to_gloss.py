import re

from fastapi import HTTPException

from app.services.language.vocabulary import (
    CONTEXTS_PATH,
    VOCABULARY_PATH,
    Vocabulary,
    load_vocabulary,
)


VOCABULARY = load_vocabulary(VOCABULARY_PATH, CONTEXTS_PATH)
ALLOWED_GLOSSES = VOCABULARY.glosses


def _load_allowed_vocabulary():
    """Compatibility helper backed by the shared items contract."""
    return load_vocabulary(VOCABULARY_PATH).glosses


# Optional synonyms do not expand the vocabulary loaded from shared data.
KEYWORD_ALIASES = {
    "medication": "MEDICINE",
    "ill": "SICK",
    "cash": "MONEY",
    "yeah": "YES",
    "yep": "YES",
    "ache": "PAIN",
    "hurt": "PAIN",
}
KEYWORD_MAP = {**VOCABULARY.keywords, **KEYWORD_ALIASES}


def text_to_gloss(
    text: str,
    context: str | None = None,
    *,
    vocabulary: Vocabulary = VOCABULARY,
) -> list[str]:
    """
    Deterministic Phase-3 fallback.

    It is deliberately vocabulary-constrained.
    Later, Rishi can place an LLM behind the same function/service
    boundary without changing the frontend contract.
    """

    if not text:
        return []

    allowed_glosses = vocabulary.glosses
    if context is not None:
        context = context.strip().lower()
        if context not in vocabulary.contexts:
            raise HTTPException(
                status_code=400,
                detail="Unknown vocabulary context.",
            )
        allowed_glosses = vocabulary.contexts[context]

    words = re.findall(
        r"[a-zA-Z']+",
        text.lower(),
    )

    result = []

    for word in words:
        gloss = vocabulary.keywords.get(word) or KEYWORD_ALIASES.get(word)

        if (
            gloss
            and gloss in allowed_glosses
            and gloss not in result
        ):
            result.append(gloss)

    return result

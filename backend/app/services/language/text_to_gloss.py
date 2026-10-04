import json
import re
from pathlib import Path


BACKEND_ROOT = Path(
    __file__
).resolve().parents[3]

VOCABULARY_PATH = (
    BACKEND_ROOT.parent
    / "shared"
    / "vocabulary"
    / "vocabulary.json"
)


FALLBACK_VOCABULARY = {
    "DOCTOR",
    "PATIENT",
    "MEDICINE",
    "SICK",
    "YESTERDAY",
    "BANK",
    "MONEY",
    "YES",
    "NO",
    "WHERE",
    "HELP",
    "PAIN",
}


def _load_allowed_vocabulary():
    try:
        payload = json.loads(
            VOCABULARY_PATH.read_text(
                encoding="utf-8"
            )
        )

        return {
            item["gloss"].upper()
            for item in payload.get(
                "vocabulary",
                []
            )
            if "gloss" in item
        }
    except (
        OSError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
    ):
        return FALLBACK_VOCABULARY


ALLOWED_GLOSSES = (
    _load_allowed_vocabulary()
)


KEYWORD_MAP = {
    "doctor": "DOCTOR",
    "patient": "PATIENT",
    "medicine": "MEDICINE",
    "medication": "MEDICINE",
    "sick": "SICK",
    "ill": "SICK",
    "yesterday": "YESTERDAY",
    "bank": "BANK",
    "money": "MONEY",
    "cash": "MONEY",
    "yes": "YES",
    "yeah": "YES",
    "yep": "YES",
    "no": "NO",
    "where": "WHERE",
    "help": "HELP",
    "pain": "PAIN",
    "ache": "PAIN",
}


def text_to_gloss(
    text: str,
) -> list[str]:
    """
    Deterministic Phase-3 fallback.

    It is deliberately vocabulary-constrained.
    Later, Rishi can place an LLM behind the same function/service
    boundary without changing the frontend contract.
    """

    if not text:
        return []

    words = re.findall(
        r"[a-zA-Z']+",
        text.lower(),
    )

    result = []

    for word in words:
        gloss = KEYWORD_MAP.get(word)

        if (
            gloss
            and gloss in ALLOWED_GLOSSES
            and gloss not in result
        ):
            result.append(gloss)

    return result

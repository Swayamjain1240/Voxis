from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable, Iterable

from app.services.language.text_to_gloss import VOCABULARY, text_to_gloss


@dataclass(frozen=True)
class GlossConversionResult:
    glosses: list[str]
    unsupported: list[str]
    source: str
    vocabulary_version: str

    def as_dict(self) -> dict[str, object]:
        return {
            "glosses": self.glosses,
            "unsupported": self.unsupported,
            "source": self.source,
            "vocabulary_version": self.vocabulary_version,
        }


def validate_gloss_tokens(
    tokens: Iterable[Any],
    *,
    context: str | None = None,
) -> tuple[list[str], list[str]]:
    allowed = VOCABULARY.glosses if context is None else VOCABULARY.contexts.get(context)
    if allowed is None:
        raise ValueError("Unknown vocabulary context.")
    accepted: list[str] = []
    unsupported: list[str] = []
    for token in tokens:
        normalized = str(token).strip().upper()
        if not normalized:
            continue
        if normalized in allowed:
            if normalized not in accepted:
                accepted.append(normalized)
        elif normalized not in unsupported:
            unsupported.append(normalized)
    return accepted, unsupported


def _tokens_from_generator_output(output: Any) -> list[Any]:
    if isinstance(output, dict):
        return output.get("glosses", [])
    if isinstance(output, str):
        return re.findall(r"[A-Z][A-Z0-9_]*", output.upper())
    if isinstance(output, (list, tuple)):
        return list(output)
    raise ValueError("Gloss generator output must be a list, string, or object.")


def convert_text_to_gloss(
    text: str,
    context: str | None = None,
    *,
    generator: Callable[[str, str | None], Any] | None = None,
) -> GlossConversionResult:
    if generator is None:
        tokens = text_to_gloss(text, context=context)
        source = "deterministic"
    else:
        try:
            tokens = _tokens_from_generator_output(generator(text, context))
            source = "llm"
        except Exception:
            tokens = text_to_gloss(text, context=context)
            source = "deterministic_fallback"
    accepted, unsupported = validate_gloss_tokens(tokens, context=context)
    return GlossConversionResult(
        glosses=accepted,
        unsupported=unsupported,
        source=source,
        vocabulary_version=VOCABULARY.version,
    )

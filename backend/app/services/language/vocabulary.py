import json
import re
from dataclasses import dataclass
from pathlib import Path


VOCABULARY_DIRECTORY = (
    Path(__file__).resolve().parents[4]
    / "shared"
    / "vocabulary"
)
VOCABULARY_PATH = VOCABULARY_DIRECTORY / "vocabulary.json"
CONTEXTS_PATH = VOCABULARY_DIRECTORY / "contexts.json"


@dataclass(frozen=True)
class Vocabulary:
    version: str
    glosses: frozenset[str]
    keywords: dict[str, str]
    contexts: dict[str, frozenset[str]]
    default_context: str | None = None


def load_vocabulary(
    vocabulary_path: str | Path = VOCABULARY_PATH,
    contexts_path: str | Path | None = None,
) -> Vocabulary:
    """Load the shared items contract; invalid/missing data never adds a fallback."""
    vocabulary_path = Path(vocabulary_path)
    # Shared JSON may have a UTF-8 BOM, particularly in Windows checkouts.
    payload = json.loads(vocabulary_path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("Vocabulary must be an object.")

    version = payload.get("version")
    items = payload.get("items")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("Vocabulary must have a version.")
    if not isinstance(items, list) or not items:
        raise ValueError("Vocabulary must contain a non-empty items list.")

    glosses: set[str] = set()
    keywords: dict[str, str] = {}
    item_contexts: dict[str, set[str]] = {}

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Vocabulary items must be objects.")
        gloss = item.get("gloss")
        if not isinstance(gloss, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", gloss):
            raise ValueError("Vocabulary glosses must be uppercase labels.")
        if gloss in glosses:
            raise ValueError("Vocabulary glosses must be unique.")
        glosses.add(gloss)

        text = item.get("text", gloss)
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Vocabulary text must be a non-empty string.")
        for keyword in (gloss.lower(), text.strip().lower()):
            if keyword in keywords and keywords[keyword] != gloss:
                raise ValueError("Vocabulary keywords must map to one gloss.")
            keywords[keyword] = gloss

        contexts = item.get("contexts", [])
        if not isinstance(contexts, list) or any(
            not isinstance(context, str) or not context.strip()
            for context in contexts
        ):
            raise ValueError("Item contexts must be a list of context names.")
        for context in contexts:
            normalized_context = context.strip().lower()
            item_contexts.setdefault(normalized_context, set()).add(gloss)

    allowed_contexts = {
        name: frozenset(allowed)
        for name, allowed in item_contexts.items()
    }
    default_context = None
    if contexts_path is not None:
        contexts_path = Path(contexts_path)
        if contexts_path.exists():
            context_payload = json.loads(
                contexts_path.read_text(encoding="utf-8-sig")
            )
            if not isinstance(context_payload, dict) or (
                context_payload.get("version") is not None
                and context_payload.get("version") != version
            ):
                raise ValueError(
                    "Contexts must use the active vocabulary version."
                )
            contexts = context_payload.get("contexts")
            if not isinstance(contexts, dict):
                raise ValueError("Contexts must contain a contexts object.")
            allowed_contexts = {}
            for name, definition in contexts.items():
                if (
                    not isinstance(name, str)
                    or not name.strip()
                    or not isinstance(definition, dict)
                ):
                    raise ValueError(
                        "Each context must have a name and an object definition."
                    )
                normalized_name = name.strip().lower()
                allowed = definition.get("allowed_glosses")
                if not isinstance(allowed, list) or any(
                    not isinstance(gloss, str) or gloss not in glosses
                    for gloss in allowed
                ):
                    raise ValueError(
                        "Context allowlists must contain only active vocabulary glosses."
                    )
                allowed_contexts[normalized_name] = frozenset(allowed)
            default_context = context_payload.get("default_context")
            if default_context is not None:
                if not isinstance(default_context, str):
                    raise ValueError("The default context must be a string.")
                default_context = default_context.strip().lower()
                if default_context not in allowed_contexts:
                    raise ValueError(
                        "The default context must be defined in contexts."
                    )

    return Vocabulary(
        version=version,
        glosses=frozenset(glosses),
        keywords=keywords,
        contexts=allowed_contexts,
        default_context=default_context,
    )


def load_label_map(vocabulary: Vocabulary, path: Path = VOCABULARY_DIRECTORY / "label_map.json") -> dict[str, int]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    labels = payload.get("gloss_to_label", {})
    if payload.get("version") != vocabulary.version or set(labels) != vocabulary.glosses:
        raise ValueError("Label map must match the active vocabulary and version.")
    if any(type(index) is not int for index in labels.values()):
        raise ValueError("Class labels must be integers.")
    if sorted(labels.values()) != list(range(len(labels))):
        raise ValueError("Class labels must be unique and contiguous.")
    if payload.get("labels") != {str(index): gloss for gloss, index in labels.items()}:
        raise ValueError("Label map directions must agree.")
    return labels

from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import (
    AfterValidator, AwareDatetime, BaseModel, BeforeValidator, ConfigDict, Field,
    WithJsonSchema,
)

from app.services.language.text_to_gloss import VOCABULARY


SCHEMA_VERSION = "1.0.0"


class ContractModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True, allow_inf_nan=False,
        validate_default=True,
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def legacy_timestamp(value):
    # Compatibility with the original client: numeric timestamps mean milliseconds.
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if not 0 <= value <= 253402300799000:
            raise ValueError("Timestamp is outside the supported range.")
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
    return value


def safe_text(value: str) -> str:
    if any((ord(char) < 32 and char not in "\t\n\r") or ord(char) == 127 for char in value):
        raise ValueError("Text contains unsupported control characters.")
    return value


def known_gloss(value: str) -> str:
    if value not in VOCABULARY.glosses:
        raise ValueError("Gloss is not in the active vocabulary.")
    return value


def known_context(value: str) -> str:
    if value not in VOCABULARY.contexts:
        raise ValueError("Unknown vocabulary context.")
    return value


Identifier = Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_:-]+$")]
Text = Annotated[str, Field(min_length=1, max_length=4000), AfterValidator(safe_text)]
Gloss = Annotated[
    str, AfterValidator(known_gloss),
    WithJsonSchema({"type": "string", "enum": sorted(VOCABULARY.glosses)}),
]
Context = Annotated[
    str, AfterValidator(known_context),
    WithJsonSchema({"type": "string", "enum": sorted(VOCABULARY.contexts)}),
]
GlossList = Annotated[list[Gloss], Field(max_length=60)]
Timestamp = Annotated[
    AwareDatetime, BeforeValidator(legacy_timestamp),
    AfterValidator(lambda value: value.astimezone(timezone.utc)),
]
Version = Literal["1.0.0"]

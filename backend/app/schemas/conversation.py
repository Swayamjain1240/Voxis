from typing import Literal

from pydantic import AliasChoices, Field, model_validator

from app.schemas.common import (
    Context, ContractModel, GlossList, Identifier, Text, Timestamp, Version, utc_now,
)
from app.services.language.text_to_gloss import VOCABULARY


class ConversationMessage(ContractModel):
    message_id: Identifier = Field(validation_alias=AliasChoices("message_id", "id"))
    schema_version: Version = "1.0.0"
    vocabulary_version: Version = "1.0.0"
    sender: Literal["user", "system", "rishi_pipeline", "swayam_pipeline"] = "user"
    source: Literal["speech", "sign", "text", "system"]
    modality: Literal["speech", "sign", "text", "avatar"] = "text"
    text: Text
    glosses: GlossList = Field(default_factory=list)
    context: Context | None = None
    timestamp: Timestamp = Field(default_factory=utc_now)

    @model_validator(mode="before")
    @classmethod
    def infer_modality(cls, value):
        if isinstance(value, dict) and "modality" not in value:
            value = {**value, "modality": value.get("source", "text")}
            if value["modality"] == "system":
                value["modality"] = "text"
        return value

    @model_validator(mode="after")
    def constrain_context(self):
        if self.context and any(g not in VOCABULARY.contexts[self.context] for g in self.glosses):
            raise ValueError("Gloss is not permitted in this context.")
        return self

    @property
    def id(self):
        """Legacy Python caller alias; serialized messages always use message_id."""
        return self.message_id


class ConversationInput(ConversationMessage):
    sender: Literal["user"] = "user"
    source: Literal["speech", "sign", "text"]


class ConversationTurn(ConversationMessage):
    pass


class TextToGlossRequest(ContractModel):
    text: Text
    context: Context | None = None
    language: Literal["en"] = "en"


class GlossToTextRequest(ContractModel):
    glosses: GlossList = Field(min_length=1)
    context: Context | None = None
    language: Literal["en"] = "en"

    @model_validator(mode="before")
    @classmethod
    def accept_legacy_list(cls, value):
        return {"glosses": value} if isinstance(value, list) else value

    @model_validator(mode="after")
    def constrain_context(self):
        if self.context and any(g not in VOCABULARY.contexts[self.context] for g in self.glosses):
            raise ValueError("Gloss is not permitted in this context.")
        return self

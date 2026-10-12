from typing import Annotated, Literal

from pydantic import Field, model_validator

from app.schemas.common import (
    Context, ContractModel, Gloss, Identifier, Timestamp, Version, utc_now,
)
from app.services.language.text_to_gloss import VOCABULARY
from app.services.language.vocabulary import load_label_map


LABEL_MAP = load_label_map(VOCABULARY)


class SignPrediction(ContractModel):
    label: int = Field(ge=-1, le=len(LABEL_MAP) - 1, strict=True)
    gloss: Gloss | Literal["UNKNOWN"]
    confidence: float = Field(ge=0.0, le=1.0)
    stable: bool

    @model_validator(mode="after")
    def unknown_is_not_stable(self):
        if self.gloss == "UNKNOWN" and (self.label != -1 or self.stable):
            raise ValueError("UNKNOWN must have label -1 and cannot be stable.")
        if self.gloss != "UNKNOWN" and self.label != LABEL_MAP[self.gloss]:
            raise ValueError("Prediction label must match the shared label map.")
        return self


class SignPredictionResult(ContractModel):
    type: Literal["sign_prediction"] = "sign_prediction"
    schema_version: Version = "1.0.0"
    vocabulary_version: Version = "1.0.0"
    model_version: Annotated[str, Field(min_length=1, max_length=64)]
    prediction: SignPrediction
    sequence_id: Identifier
    timestamp: Timestamp = Field(default_factory=utc_now)


Feature = Annotated[float, Field(strict=True, allow_inf_nan=False)]
Frame = Annotated[list[Feature], Field(min_length=300, max_length=300)]


class SignInferenceRequest(ContractModel):
    # Raw canonical left hand / right hand / pose, x/y/z/visibility, 60 frames.
    # Preprocessing belongs to the eventual runtime, not to this request parser.
    frames: Annotated[list[Frame], Field(min_length=60, max_length=60)]
    sequence_length: Literal[60] = 60
    top_k: int = Field(default=3, ge=1, le=10, strict=True)
    context: Context | None = None
    vocabulary_version: Version = "1.0.0"

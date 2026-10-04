from pydantic import BaseModel, Field


class SignPrediction(BaseModel):
    gloss: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


class SignPredictionResult(BaseModel):
    glosses: list[str]
    confidence: list[float]
    source: str = "sign"
    timestamp: int


class SignInferenceRequest(BaseModel):
    frames: list[list[float]] = Field(
        default_factory=list
    )

    sequence_length: int = Field(
        default=60,
        ge=1,
        le=240,
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
    )

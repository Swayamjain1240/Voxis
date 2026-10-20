from app.core.config import settings
from app.core.exceptions import (
    FeatureNotEnabledError,
    FeatureUnavailableError,
)
from app.core.config import settings
from app.schemas.sign import SignPredictionResult
from app.services.language.text_to_gloss import VOCABULARY
from app.services.language.vocabulary import load_label_map
from app.services.sign_recognition.model_loader import SignModelLoader


class SignInferenceService:
    """
    Runtime boundary for Swayam's sign model.

    Rishi's pipeline never imports the trained model directly.
    It consumes the shared sign-prediction contract instead.
    """

    def __init__(self, enabled: bool | None = None, loader: SignModelLoader | None = None):
        self.enabled = (
            settings.sign_model_enabled
            if enabled is None
            else enabled
        )
        self.loader = loader or SignModelLoader(settings.sign_model_path)

    @property
    def implemented(self) -> bool:
        return True

    def status(self):
        state = "disabled" if not self.enabled else "available" if self.loader.loaded else "unavailable"
        return {
            "enabled": self.enabled,
            "implemented": self.implemented,
            "available": self.enabled and self.loader.loaded,
            "status": state,
            "model_loaded": self.loader.loaded,
            "runtime": "onnxruntime" if self.loader.loaded else "not-loaded",
        }

    async def predict(
        self,
        payload: dict,
    ):
        if not self.enabled:
            raise FeatureNotEnabledError(
                "Sign recognition",
                "Phase 3",
            )

        try:
            probabilities = self.loader.predict(payload["frames"])
        except (RuntimeError, OSError, ValueError) as error:
            raise FeatureUnavailableError(
                "Sign recognition",
                "SIGN_MODEL_UNAVAILABLE",
                "The configured sign model is not available for inference.",
            ) from error

        label_map = load_label_map(VOCABULARY)
        inverse_label_map = {index: gloss for gloss, index in label_map.items()}
        ranking = sorted(range(len(probabilities)), key=probabilities.__getitem__, reverse=True)
        top_index = ranking[0]
        confidence = float(probabilities[top_index])
        margin = confidence - float(probabilities[ranking[1]])
        accepted = (
            confidence >= settings.sign_confidence_threshold
            and margin >= settings.sign_margin_threshold
        )
        gloss = inverse_label_map[top_index] if accepted else "UNKNOWN"
        label = top_index if accepted else -1
        return SignPredictionResult(
            model_version=str(self.loader.metadata["model_version"]),
            sequence_id=payload.get("sequence_id", "sequence"),
            prediction={
                "label": label,
                "gloss": gloss,
                "confidence": confidence,
                "stable": accepted,
            },
        )

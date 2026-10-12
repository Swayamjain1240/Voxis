from app.core.config import settings
from app.core.exceptions import (
    FeatureNotEnabledError,
    FeatureUnavailableError,
)


class SignInferenceService:
    """
    Runtime boundary for Swayam's sign model.

    Rishi's pipeline never imports the trained model directly.
    It consumes the shared sign-prediction contract instead.
    """

    def __init__(self, enabled: bool | None = None):
        self.enabled = (
            settings.sign_model_enabled
            if enabled is None
            else enabled
        )

    @property
    def implemented(self) -> bool:
        return False

    def status(self):
        state = (
            "disabled"
            if not self.enabled
            else "unavailable"
            if not self.implemented
            else "available"
        )
        return {
            "enabled": self.enabled,
            "implemented": self.implemented,
            "available": self.enabled and self.implemented,
            "status": state,
            "model_loaded": False,
            "runtime": "not-implemented",
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

        raise FeatureUnavailableError(
            "Sign recognition",
            "SIGN_MODEL_UNAVAILABLE",
        )

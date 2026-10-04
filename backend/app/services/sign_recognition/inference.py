import time

from app.core.config import settings
from app.core.exceptions import (
    FeatureNotEnabledError,
)


class SignInferenceService:
    """
    Runtime boundary for Swayam's sign model.

    Rishi's pipeline never imports the trained model directly.
    It consumes the shared sign-prediction contract instead.
    """

    def __init__(self):
        self.enabled = (
            settings.sign_model_enabled
        )

    def status(self):
        return {
            "enabled": self.enabled,
            "model_loaded": False,
            "runtime": "pending-phase-3",
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

        frames = payload.get(
            "frames",
            []
        )

        return {
            "glosses": [],
            "confidence": [],
            "source": "sign",
            "timestamp": int(
                time.time() * 1000
            ),
            "frames_received": len(frames),
        }

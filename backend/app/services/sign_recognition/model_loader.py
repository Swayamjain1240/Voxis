from pathlib import Path


class SignModelLoader:
    """
    Loads the trained sign model in the final runtime.

    The actual ONNX/model implementation is intentionally deferred
    until Swayam completes Phase 3 and Phase 6 export.
    """

    def __init__(
        self,
        model_path: str | None = None,
    ):
        self.model_path = (
            Path(model_path)
            if model_path
            else None
        )

        self.model = None

    @property
    def loaded(self) -> bool:
        return self.model is not None

    def load(self):
        if (
            not self.model_path
            or not self.model_path.exists()
        ):
            return None

        # Future:
        # self.model = ort.InferenceSession(...)
        return None

    def unload(self):
        self.model = None

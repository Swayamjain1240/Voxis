from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from app.services.language.text_to_gloss import VOCABULARY
from app.services.language.vocabulary import load_label_map


EXPECTED_SEQUENCE_LENGTH = 60
EXPECTED_FEATURES = 300


class SignModelLoader:
    """Lazy ONNX Runtime loader with sidecar metadata validation."""

    def __init__(self, model_path: str | None = None, session: Any | None = None):
        self.model_path = Path(model_path) if model_path else None
        self.model = session
        self.metadata: dict[str, object] | None = None
        self._load_error = ""
        if session is not None:
            self.metadata = {
                "model_version": "injected-test-model",
                "vocabulary_version": VOCABULARY.version,
                "preprocessing_version": "1.0.0",
                "sequence_length": EXPECTED_SEQUENCE_LENGTH,
                "input_features": EXPECTED_FEATURES,
            }

    @property
    def loaded(self) -> bool:
        return self.model is not None and self.metadata is not None

    @staticmethod
    def _read_sidecars(model_path: Path) -> dict[str, object]:
        metadata_path = model_path.with_name("model_metadata.json")
        label_map_path = model_path.with_name("label_map.json")
        if not metadata_path.exists() or not label_map_path.exists():
            raise ValueError("Sign model metadata sidecars are required.")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
        label_map = json.loads(label_map_path.read_text(encoding="utf-8-sig"))
        expected_labels = load_label_map(VOCABULARY)
        if metadata.get("vocabulary_version") != VOCABULARY.version:
            raise ValueError("Sign model vocabulary version does not match the shared map.")
        if metadata.get("preprocessing_version") != "1.0.0":
            raise ValueError("Sign model preprocessing version is not supported.")
        if metadata.get("sequence_length") != EXPECTED_SEQUENCE_LENGTH or metadata.get("input_features") != EXPECTED_FEATURES:
            raise ValueError("Sign model input shape must be 60 frames by 300 features.")
        if label_map.get("gloss_to_label") != expected_labels:
            raise ValueError("Sign model label map does not match the shared map.")
        metadata["label_map"] = expected_labels
        return metadata

    def load(self):
        if self.loaded:
            return self.model
        if not self.model_path or not self.model_path.exists():
            return None
        try:
            import onnxruntime as ort

            self.model = ort.InferenceSession(
                str(self.model_path),
                providers=["CPUExecutionProvider"],
            )
            self.metadata = self._read_sidecars(self.model_path)
        except ImportError as error:
            self._load_error = "Install the optional onnxruntime runtime."
            self.model = None
            raise RuntimeError(self._load_error) from error
        except Exception:
            self.model = None
            self.metadata = None
            raise
        return self.model

    @staticmethod
    def _validate_frames(frames: list[list[float]]) -> None:
        if len(frames) != EXPECTED_SEQUENCE_LENGTH or any(
            len(frame) != EXPECTED_FEATURES for frame in frames
        ):
            raise ValueError("Sign model input must be exactly 60 frames by 300 features.")
        if any(not math.isfinite(float(value)) for frame in frames for value in frame):
            raise ValueError("Sign model input must contain only finite values.")

    def predict(self, frames: list[list[float]]) -> list[float]:
        if not self.loaded:
            self.load()
        if not self.loaded:
            raise RuntimeError("Sign model is not loaded.")
        self._validate_frames(frames)
        input_name = self.model.get_inputs()[0].name
        outputs = self.model.run(None, {input_name: [frames]})
        logits = outputs[0].tolist()[0]
        if len(logits) != len(load_label_map(VOCABULARY)):
            raise ValueError("Sign model output class count does not match the vocabulary.")
        maximum = max(float(value) for value in logits)
        exponentials = [math.exp(float(value) - maximum) for value in logits]
        total = sum(exponentials)
        return [value / total for value in exponentials]

    def unload(self):
        self.model = None
        self.metadata = None

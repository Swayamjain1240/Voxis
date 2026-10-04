from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np


LEFT_HAND_COUNT = 21
RIGHT_HAND_COUNT = 21
POSE_COUNT = 33

FEATURES_PER_POINT = 4
TOTAL_FEATURES = (
    LEFT_HAND_COUNT
    + RIGHT_HAND_COUNT
    + POSE_COUNT
) * FEATURES_PER_POINT


@dataclass
class ExtractionResult:
    video_path: str
    frames: np.ndarray
    fps: float
    frame_count: int
    feature_size: int = TOTAL_FEATURES


class MediaPipeExtractor:
    """
    Extracts:
        left hand  : 21 landmarks
        right hand : 21 landmarks
        pose       : 33 landmarks

    Every landmark is represented as:
        x, y, z, visibility

    Output per frame:
        75 points ? 4 = 300 features
    """

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        try:
            import mediapipe as mp
        except ImportError as exc:
            raise RuntimeError(
                "MediaPipe is not installed. "
                "Run: pip install mediapipe"
            ) from exc

        if not hasattr(mp, "solutions"):
            raise RuntimeError(
                "The installed MediaPipe build does not expose "
                "the legacy solutions API expected by this extractor."
            )

        self.mp = mp

        self.holistic = mp.solutions.holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            refine_face_landmarks=False,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    @staticmethod
    def _landmark_array(
        landmarks: Any,
        count: int,
        default_visibility: float = 0.0,
    ) -> np.ndarray:
        output = np.zeros(
            (count, FEATURES_PER_POINT),
            dtype=np.float32,
        )

        if landmarks is None:
            output[:, 3] = default_visibility
            return output

        for index in range(
            min(len(landmarks.landmark), count)
        ):
            landmark = landmarks.landmark[index]

            output[index] = [
                float(landmark.x),
                float(landmark.y),
                float(landmark.z),
                float(
                    getattr(
                        landmark,
                        "visibility",
                        1.0,
                    )
                ),
            ]

        return output

    def _process_frame(
        self,
        frame: np.ndarray,
    ) -> np.ndarray:

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        result = self.holistic.process(rgb)

        left_hand = self._landmark_array(
            result.left_hand_landmarks,
            LEFT_HAND_COUNT,
        )

        right_hand = self._landmark_array(
            result.right_hand_landmarks,
            RIGHT_HAND_COUNT,
        )

        pose = self._landmark_array(
            result.pose_landmarks,
            POSE_COUNT,
        )

        combined = np.concatenate(
            [
                left_hand,
                right_hand,
                pose,
            ],
            axis=0,
        )

        return combined.reshape(-1)

    def extract_video(
        self,
        video_path: str | Path,
    ) -> ExtractionResult:

        path = Path(video_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Video not found: {path}"
            )

        capture = cv2.VideoCapture(
            str(path)
        )

        if not capture.isOpened():
            raise RuntimeError(
                f"Could not open video: {path}"
            )

        fps = (
            capture.get(
                cv2.CAP_PROP_FPS
            )
            or 30.0
        )

        frames = []

        try:
            while True:
                success, frame = (
                    capture.read()
                )

                if not success:
                    break

                features = self._process_frame(
                    frame
                )

                if features.shape != (
                    TOTAL_FEATURES,
                ):
                    raise RuntimeError(
                        "Unexpected landmark feature size: "
                        f"{features.shape}"
                    )

                frames.append(features)

        finally:
            capture.release()

        sequence = (
            np.asarray(
                frames,
                dtype=np.float32,
            )
            if frames
            else np.empty(
                (0, TOTAL_FEATURES),
                dtype=np.float32,
            )
        )

        return ExtractionResult(
            video_path=str(path),
            frames=sequence,
            fps=float(fps),
            frame_count=len(sequence),
        )

    def close(self):
        self.holistic.close()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self.close()

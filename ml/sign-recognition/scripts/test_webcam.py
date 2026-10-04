from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

from src.extraction.mediapipe_extractor import (
    MediaPipeExtractor,
)


def draw_status(
    frame,
    text,
):
    cv2.rectangle(
        frame,
        (10, 10),
        (500, 55),
        (0, 0, 0),
        -1,
    )

    cv2.putText(
        frame,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )


def main():
    parser = argparse.ArgumentParser(
        description="VOXIS MediaPipe webcam test"
    )

    parser.add_argument(
        "--camera",
        type=int,
        default=0,
    )

    parser.add_argument(
        "--save",
        type=Path,
        default=None,
    )

    args = parser.parse_args()

    camera = cv2.VideoCapture(
        args.camera
    )

    if not camera.isOpened():
        raise RuntimeError(
            f"Could not open camera {args.camera}"
        )

    recorder = None

    if args.save:
        width = int(
            camera.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            camera.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        fps = (
            camera.get(
                cv2.CAP_PROP_FPS
            )
            or 30.0
        )

        args.save.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        recorder = cv2.VideoWriter(
            str(args.save),
            cv2.VideoWriter_fourcc(
                *"mp4v"
            ),
            fps,
            (width, height),
        )

    # MediaPipe is imported/initialized through the extractor.
    with MediaPipeExtractor() as extractor:
        try:
            while True:
                success, frame = (
                    camera.read()
                )

                if not success:
                    break

                features = (
                    extractor._process_frame(
                        frame
                    )
                )

                hands_present = np.any(
                    np.abs(
                        features[
                            : 42 * 4
                        ]
                    )
                    > 1e-6
                )

                pose_present = np.any(
                    np.abs(
                        features[
                            42 * 4:
                        ]
                    )
                    > 1e-6
                )

                status = (
                    f"Hands: "
                    f"{'YES' if hands_present else 'NO'} | "
                    f"Pose: "
                    f"{'YES' if pose_present else 'NO'} | "
                    f"Features: {len(features)}"
                )

                draw_status(
                    frame,
                    status,
                )

                if recorder:
                    recorder.write(
                        frame
                    )

                cv2.imshow(
                    "VOXIS MediaPipe Test",
                    frame,
                )

                key = (
                    cv2.waitKey(1)
                    & 0xFF
                )

                if key in (
                    ord("q"),
                    ord("Q"),
                ):
                    break

        finally:
            camera.release()

            if recorder:
                recorder.release()

            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

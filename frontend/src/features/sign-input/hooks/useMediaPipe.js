import { useCallback, useState } from "react";

/*
 * MediaPipe adapter boundary.
 *
 * Swayam can connect the actual MediaPipe Tasks Vision processor
 * without changing CameraFeed or the rest of the application.
 *
 * Input:
 *   processing result from MediaPipe
 *
 * Output:
 *   landmarks suitable for LandmarkOverlay / frameBuffer
 */

export default function useMediaPipe() {
  const [status, setStatus] = useState("not_initialized");
  const [landmarks, setLandmarks] = useState([]);

  const initialize = useCallback(async () => {
    setStatus("ready");
  }, []);

  const processResult = useCallback((result) => {
    const combined = [
      ...(result?.leftHandLandmarks || []),
      ...(result?.rightHandLandmarks || []),
      ...(result?.poseLandmarks || []),
    ];

    setLandmarks(combined);

    return combined;
  }, []);

  const reset = useCallback(() => {
    setLandmarks([]);
    setStatus("not_initialized");
  }, []);

  return {
    status,
    landmarks,
    initialize,
    processResult,
    reset,
  };
}

import { useCallback, useRef, useState } from "react";

import { mediaPipeConfig } from "../../../config/env.js";
import {
  canonicalizeLandmarks,
  hasDetectedLandmarks,
} from "../services/landmarkExtractor";

const NOT_CONFIGURED_MESSAGE =
  "MediaPipe is not configured. Add a local model and WASM asset path to frontend/.env.";

function firstLandmarks(value) {
  return Array.isArray(value?.[0]) ? value[0] : value || [];
}

/** Convert Tasks Vision holistic output into the app's adapter result shape. */
export function mapHolisticResult(result = {}) {
  return {
    leftHandLandmarks: firstLandmarks(result.leftHandLandmarks),
    rightHandLandmarks: firstLandmarks(result.rightHandLandmarks),
    poseLandmarks: firstLandmarks(result.poseLandmarks),
  };
}

export function createProcessorOptions(config = mediaPipeConfig) {
  return {
    baseOptions: {
      modelAssetPath: config.modelAssetPath,
      delegate: "CPU",
    },
    runningMode: "VIDEO",
    minPoseDetectionConfidence: 0.5,
    minPosePresenceConfidence: 0.5,
    minHandLandmarksConfidence: 0.5,
  };
}

export default function useMediaPipe(config = mediaPipeConfig) {
  const processorRef = useRef(null);
  const [status, setStatus] = useState("not_initialized");
  const [error, setError] = useState("");
  const [landmarks, setLandmarks] = useState([]);
  const [lastResult, setLastResult] = useState(null);

  const initialize = useCallback(async () => {
    if (!config.configured) {
      setStatus("not_configured");
      setError(NOT_CONFIGURED_MESSAGE);
      return false;
    }

    try {
      setStatus("initializing");
      setError("");
      const { FilesetResolver, HolisticLandmarker } = await import(
        "@mediapipe/tasks-vision"
      );
      const vision = await FilesetResolver.forVisionTasks(config.wasmRoot);
      processorRef.current = await HolisticLandmarker.createFromOptions(
        vision,
        createProcessorOptions(config)
      );
      setStatus("ready");
      return true;
    } catch (initializationError) {
      processorRef.current = null;
      setStatus("error");
      setError(
        initializationError?.message ||
          "MediaPipe could not initialize with the configured assets."
      );
      return false;
    }
  }, [config]);

  const processResult = useCallback((rawResult) => {
    const result = mapHolisticResult(rawResult);
    const nextLandmarks = canonicalizeLandmarks(result);
    setLandmarks(nextLandmarks);
    setLastResult(result);
    setStatus(hasDetectedLandmarks(result) ? "tracking" : "no_detection");
    return result;
  }, []);

  const processVideo = useCallback(
    (video, timestamp = performance.now()) => {
      if (!processorRef.current) {
        return null;
      }
      const result = processorRef.current.detectForVideo(video, timestamp);
      return processResult(result);
    },
    [processResult]
  );

  const reset = useCallback(() => {
    processorRef.current?.close?.();
    processorRef.current = null;
    setLandmarks([]);
    setLastResult(null);
    setError("");
    setStatus("not_initialized");
  }, []);

  return {
    status,
    error,
    landmarks,
    lastResult,
    isReady: status === "ready" || status === "tracking" || status === "no_detection",
    initialize,
    processResult,
    processVideo,
    reset,
  };
}

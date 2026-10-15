import { useCallback, useEffect, useRef, useState } from "react";

import useCamera from "./useCamera";
import useMediaPipe from "./useMediaPipe";
import { FrameBuffer } from "../services/frameBuffer";
import {
  flattenCanonicalFrame,
  hasDetectedLandmarks,
} from "../services/landmarkExtractor";
import { isCanonicalSequence } from "../services/sequence";

export function isVideoReadyForCapture(video) {
  return Boolean(
    video &&
      video.readyState >= 2 &&
      video.videoWidth > 0 &&
      video.videoHeight > 0
  );
}

export default function useSignCapture() {
  const camera = useCamera();
  const mediaPipe = useMediaPipe();
  const {
    isActive: cameraIsActive,
    startCamera,
    stopCamera,
  } = camera;
  const {
    isReady: mediaPipeIsReady,
    initialize,
    processVideo,
    reset,
  } = mediaPipe;
  const videoRef = useRef(null);
  const frameBufferRef = useRef(new FrameBuffer());
  const animationFrameRef = useRef(null);
  const [frameCount, setFrameCount] = useState(0);
  const [sequence, setSequence] = useState(null);
  const [captureStatus, setCaptureStatus] = useState("idle");
  const [captureError, setCaptureError] = useState("");

  const stopLoop = useCallback(() => {
    if (animationFrameRef.current !== null) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
  }, []);

  const captureFrame = useCallback(() => {
    if (!videoRef.current || !mediaPipeIsReady) {
      return;
    }

    if (!isVideoReadyForCapture(videoRef.current)) {
      setCaptureStatus("camera_loading");
      return;
    }

    try {
      const result = processVideo(videoRef.current);
      if (result && hasDetectedLandmarks(result)) {
        const nextFrame = flattenCanonicalFrame(result);
        frameBufferRef.current.push(nextFrame);
        setFrameCount(frameBufferRef.current.size());
        if (frameBufferRef.current.isFull()) {
          const nextSequence = frameBufferRef.current.sequence();
          if (!isCanonicalSequence(nextSequence)) {
            throw new Error("The buffered sequence failed the canonical shape check.");
          }
          setSequence(nextSequence);
          setCaptureStatus("sequence_ready");
        } else {
          setCaptureStatus("capturing");
        }
      } else {
        setCaptureStatus("no_detection");
      }
      setCaptureError("");
    } catch (captureError) {
      setCaptureStatus("error");
      setCaptureError(
        captureError?.message || "The camera frame could not be processed."
      );
    }
  }, [mediaPipeIsReady, processVideo]);

  const runLoop = useCallback(() => {
    captureFrame();
    animationFrameRef.current = requestAnimationFrame(runLoop);
  }, [captureFrame]);

  const start = useCallback(async () => {
    setCaptureStatus("starting");
    setCaptureError("");
    const nextStream = await startCamera();
    if (!nextStream) {
      setCaptureStatus("camera_error");
      return false;
    }
    const initialized = await initialize();
    if (!initialized) {
      setCaptureStatus("media_pipe_error");
      return false;
    }
    setCaptureStatus("camera_loading");
    return true;
  }, [initialize, startCamera]);

  const stop = useCallback(() => {
    stopLoop();
    stopCamera();
    reset();
    frameBufferRef.current.clear();
    setFrameCount(0);
    setSequence(null);
    setCaptureStatus("idle");
    setCaptureError("");
  }, [reset, stopCamera, stopLoop]);

  const clearSequence = useCallback(() => {
    frameBufferRef.current.clear();
    setFrameCount(0);
    setSequence(null);
    setCaptureError("");
    setCaptureStatus(cameraIsActive ? "capturing" : "idle");
  }, [cameraIsActive]);

  useEffect(() => {
    if (
      cameraIsActive &&
      mediaPipeIsReady &&
      typeof requestAnimationFrame === "function"
    ) {
      animationFrameRef.current = requestAnimationFrame(runLoop);
    } else {
      stopLoop();
    }
    return stopLoop;
  }, [cameraIsActive, mediaPipeIsReady, runLoop, stopLoop]);

  useEffect(() => stopLoop, [stopLoop]);

  return {
    videoRef,
    camera,
    mediaPipe,
    frameCount,
    sequence,
    captureStatus,
    captureError,
    start,
    stop,
    clearSequence,
  };
}

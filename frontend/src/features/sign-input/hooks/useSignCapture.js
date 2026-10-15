import { useCallback, useEffect, useRef, useState } from "react";

import useCamera from "./useCamera";
import useMediaPipe from "./useMediaPipe";
import { FrameBuffer } from "../services/frameBuffer";
import {
  flattenCanonicalFrame,
  hasDetectedLandmarks,
} from "../services/landmarkExtractor";

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

    try {
      const result = processVideo(videoRef.current);
      if (result && hasDetectedLandmarks(result)) {
        const nextFrame = flattenCanonicalFrame(result);
        frameBufferRef.current.push(nextFrame);
        setFrameCount(frameBufferRef.current.size());
        if (frameBufferRef.current.isFull()) {
          setSequence(frameBufferRef.current.sequence());
          setCaptureStatus("sequence_ready");
        } else {
          setCaptureStatus("capturing");
        }
      } else {
        setCaptureStatus("no_detection");
      }
    } catch (captureError) {
      setCaptureStatus("error");
    }
  }, [mediaPipeIsReady, processVideo]);

  const runLoop = useCallback(() => {
    captureFrame();
    animationFrameRef.current = requestAnimationFrame(runLoop);
  }, [captureFrame]);

  const start = useCallback(async () => {
    const nextStream = await startCamera();
    if (!nextStream) {
      setCaptureStatus("camera_error");
      return false;
    }
    await initialize();
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
  }, [reset, stopCamera, stopLoop]);

  const clearSequence = useCallback(() => {
    frameBufferRef.current.clear();
    setFrameCount(0);
    setSequence(null);
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
    start,
    stop,
    clearSequence,
  };
}

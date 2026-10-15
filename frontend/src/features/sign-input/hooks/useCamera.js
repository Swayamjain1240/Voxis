import { useCallback, useEffect, useRef, useState } from "react";

export function cameraErrorMessage(cameraError) {
  if (cameraError?.name === "NotAllowedError") {
    return "Camera permission was denied. Allow camera access and try again.";
  }
  if (cameraError?.name === "NotFoundError") {
    return "No camera was found on this device.";
  }
  if (cameraError?.name === "NotReadableError") {
    return "The camera is busy or unavailable. Close other camera apps and try again.";
  }
  return cameraError?.message || "Unable to access the camera.";
}

export default function useCamera() {
  const streamRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const stopTracks = useCallback((nextStream = streamRef.current) => {
    nextStream?.getTracks?.().forEach((track) => track.stop());
    if (streamRef.current === nextStream) {
      streamRef.current = null;
    }
  }, []);

  const startCamera = useCallback(async () => {
    if (streamRef.current) {
      return streamRef.current;
    }

    if (!navigator.mediaDevices?.getUserMedia) {
      setStatus("error");
      setError("Camera access is not supported in this browser.");
      return null;
    }

    try {
      setStatus("requesting");
      setError("");
      const nextStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "user",
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });
      streamRef.current = nextStream;
      setStream(nextStream);
      setStatus("ready");
      return nextStream;
    } catch (cameraError) {
      setStatus("error");
      setError(cameraErrorMessage(cameraError));
      return null;
    }
  }, []);

  const stopCamera = useCallback(() => {
    stopTracks();
    setStream(null);
    setStatus("idle");
  }, [stopTracks]);

  useEffect(() => () => stopTracks(), [stopTracks]);

  return {
    stream,
    status,
    error,
    isActive: Boolean(stream),
    startCamera,
    stopCamera,
  };
}

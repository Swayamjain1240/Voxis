import { useCallback, useEffect, useState } from "react";

export default function useCamera() {
  const [stream, setStream] = useState(null);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const startCamera = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setStatus("error");
      setError("Camera access is not supported.");
      return;
    }

    try {
      setStatus("requesting");
      setError("");

      const nextStream =
        await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: "user",
            width: {
              ideal: 1280,
            },
            height: {
              ideal: 720,
            },
          },
          audio: false,
        });

      setStream(nextStream);
      setStatus("ready");
    } catch (cameraError) {
      setStatus("error");
      setError(
        cameraError?.message ||
          "Unable to access the camera."
      );
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach((track) =>
        track.stop()
      );
    }

    setStream(null);
    setStatus("idle");
  }, [stream]);

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) =>
          track.stop()
        );
      }
    };
  }, [stream]);

  return {
    stream,
    status,
    error,
    isActive: Boolean(stream),
    startCamera,
    stopCamera,
  };
}

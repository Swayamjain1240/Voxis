import React, { useEffect, useRef } from "react";

export default function CameraFeed({
  stream,
  mirrored = true,
  className = "",
}) {
  const videoRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;

    if (!video) {
      return;
    }

    video.srcObject = stream || null;

    if (stream) {
      video.play().catch(() => {});
    }

    return () => {
      if (video) {
        video.srcObject = null;
      }
    };
  }, [stream]);

  return (
    <video
      ref={videoRef}
      className={`camera-feed ${
        mirrored ? "mirrored" : ""
      } ${className}`}
      autoPlay
      playsInline
      muted
    />
  );
}

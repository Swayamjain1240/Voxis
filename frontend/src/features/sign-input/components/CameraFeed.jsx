import React, { forwardRef, useEffect, useRef } from "react";

const CameraFeed = forwardRef(function CameraFeed({
  stream,
  mirrored = true,
  className = "",
}, forwardedRef) {
  const internalRef = useRef(null);
  const videoRef = forwardedRef || internalRef;

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
});

export default CameraFeed;

import React from "react";

const STATUS_LABELS = Object.freeze({
  idle: "Ready",
  starting: "Starting camera",
  camera_loading: "Camera loading",
  capturing: "Capturing",
  no_detection: "No landmarks detected",
  sequence_ready: "Sequence ready",
  camera_error: "Camera unavailable",
  media_pipe_error: "Landmark processor unavailable",
  error: "Capture error",
});

export function formatSignStatus(status) {
  return STATUS_LABELS[status] || String(status || "Ready");
}

export default function SignStatus({
  status = "idle",
  gloss = "",
  confidence = 0,
}) {
  const percentage = Math.round(
    Math.max(0, Math.min(1, confidence)) * 100
  );

  return (
    <div className="sign-status" role="status" aria-live="polite">
      <span>{formatSignStatus(status)}</span>

      {gloss && (
        <strong>{gloss}</strong>
      )}

      {confidence > 0 && (
        <small>{percentage}%</small>
      )}
    </div>
  );
}

import React from "react";

export default function SignStatus({
  status = "idle",
  gloss = "",
  confidence = 0,
}) {
  const percentage = Math.round(
    Math.max(0, Math.min(1, confidence)) * 100
  );

  return (
    <div className="sign-status">
      <span>{status.toUpperCase()}</span>

      {gloss && (
        <strong>{gloss}</strong>
      )}

      {confidence > 0 && (
        <small>{percentage}%</small>
      )}
    </div>
  );
}

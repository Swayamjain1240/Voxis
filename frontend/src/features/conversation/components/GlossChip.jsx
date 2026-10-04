import React from "react";

export default function GlossChip({
  gloss,
  confidence,
}) {
  return (
    <span className="gloss-chip">
      <strong>{gloss}</strong>

      {typeof confidence === "number" && (
        <small>
          {Math.round(confidence * 100)}%
        </small>
      )}
    </span>
  );
}

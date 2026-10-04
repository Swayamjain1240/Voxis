import React from "react";

export default function ConfidenceMeter({
  value = 0,
  label = "Confidence",
  caption = "",
}) {
  const percentage = Math.round(
    Math.max(0, Math.min(1, value)) * 100
  );

  return (
    <section className="debug-card">
      <div className="debug-card-header">
        <div>
          <h3>{label}</h3>
          {caption && <p>{caption}</p>}
        </div>

        <strong>{percentage}%</strong>
      </div>

      <div className="meter">
        <span
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>
    </section>
  );
}

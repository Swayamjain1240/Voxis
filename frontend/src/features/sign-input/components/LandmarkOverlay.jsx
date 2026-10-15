import React from "react";

export default function LandmarkOverlay({
  landmarks = [],
}) {
  return (
    <div
      className="landmark-overlay"
      aria-label="MediaPipe landmark overlay"
      role="img"
    >
      {landmarks.map((landmark, index) => {
        const x = Number(landmark?.x ?? 0);
        const y = Number(landmark?.y ?? 0);
        const visibility = Number(landmark?.visibility ?? 1);

        if (visibility <= 0) {
          return null;
        }

        return (
          <span
            key={`${index}-${x}-${y}`}
            className="landmark-point"
            style={{
              left: `${x * 100}%`,
              top: `${y * 100}%`,
            }}
          />
        );
      })}
    </div>
  );
}

import React from "react";

const PIPELINE = [
  ["Microphone", "READY"],
  ["Audio Recorder", "READY"],
  ["Whisper", "PHASE 2"],
  ["Text → Gloss", "PHASE 3"],
  ["Avatar Runtime", "READY"],
  ["Gloss → Animation", "PHASE 4"],
];

export default function PipelineStatus() {
  return (
    <section className="debug-card">
      <h3>Pipeline Status</h3>

      <div className="debug-list">
        {PIPELINE.map(([name, state]) => (
          <div
            className="debug-row"
            key={name}
          >
            <span>{name}</span>
            <strong>{state}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

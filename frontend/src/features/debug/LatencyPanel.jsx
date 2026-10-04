import React from "react";

export default function LatencyPanel() {
  return (
    <section className="debug-card">
      <h3>Runtime Components</h3>

      <div className="debug-list">
        <div className="debug-row">
          <span>Browser audio capture</span>
          <strong>LOCAL</strong>
        </div>

        <div className="debug-row">
          <span>Whisper</span>
          <strong>NOT ACTIVE</strong>
        </div>

        <div className="debug-row">
          <span>Gloss engine</span>
          <strong>NOT ACTIVE</strong>
        </div>

        <div className="debug-row">
          <span>3D renderer</span>
          <strong>ACTIVE</strong>
        </div>
      </div>
    </section>
  );
}

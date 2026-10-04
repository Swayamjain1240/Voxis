import React from "react";

import ConfidenceMeter from "../../features/debug/ConfidenceMeter";
import PipelineStatus from "../../features/debug/PipelineStatus";
import LatencyPanel from "../../features/debug/LatencyPanel";

export default function DebugPage() {
  return (
    <main className="page">
      <section className="hero compact">
        <div className="hero-copy">
          <span className="eyebrow">DEVELOPER / DEBUG</span>

          <h1>Pipeline Debug</h1>

          <p>
            Internal diagnostics for Phase 1 development and future
            Speech → Sign integration.
          </p>
        </div>
      </section>

      <section className="debug-grid">
        <PipelineStatus />

        <ConfidenceMeter
          value={0}
          label="Sign Model Confidence"
          caption="Available after Phase 3"
        />

        <LatencyPanel />
      </section>
    </main>
  );
}

import React from "react";

import TurnIndicator from "../../features/conversation/components/TurnIndicator";

export default function ConversationPage() {
  return (
    <main className="page">
      <section className="hero compact">
        <div className="hero-copy">
          <span className="eyebrow">MODE 1 / CONVERSATION</span>

          <h1>Conversation</h1>

          <p>
            The final two-way conversation surface. It will connect the
            Speech → Sign and Sign → Speech pipelines in Phase 5/6.
          </p>
        </div>
      </section>

      <section className="conversation-layout">
        <section className="panel">
          <TurnIndicator turn="speech" />

          <div className="conversation-placeholder">
            <span>WAITING FOR PIPELINE</span>
            <h2>Conversation engine not connected yet</h2>
            <p>
              Phase 2 adds Whisper. Phase 3 adds restricted gloss conversion.
              Phase 4 adds real sign animations. This screen is intentionally
              separated so those modules can plug in without changing the UI
              architecture.
            </p>
          </div>
        </section>
      </section>
    </main>
  );
}

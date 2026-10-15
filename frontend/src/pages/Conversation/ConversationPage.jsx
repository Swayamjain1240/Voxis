import React, { useSyncExternalStore, useState } from "react";

import BankMode from "../../features/context-mode/BankMode";
import HospitalMode from "../../features/context-mode/HospitalMode";
import OfficeMode from "../../features/context-mode/OfficeMode";
import GlossChip from "../../features/conversation/components/GlossChip";
import Transcript from "../../features/conversation/components/Transcript";
import TurnIndicator from "../../features/conversation/components/TurnIndicator";
import { conversationStore } from "../../features/conversation/conversationStore";
import SignInputPanel from "../../features/sign-input/components/SignInputPanel";

export default function ConversationPage() {
  const state = useSyncExternalStore(
    conversationStore.subscribe,
    conversationStore.getState,
    conversationStore.getState
  );
  const [context, setContext] = useState("hospital");

  return (
    <main className="page">
      <section className="hero compact">
        <div className="hero-copy">
          <span className="eyebrow">MODE 1 / CONVERSATION FOUNDATION</span>
          <h1>Conversation</h1>
          <p>
            Local capture and conversation state are connected. AI prediction,
            Whisper transcription, and avatar translation remain disabled until
            the later fixing and build parts.
          </p>
        </div>
      </section>

      <section className="context-section" aria-labelledby="context-title">
        <div className="section-heading">
          <span className="panel-kicker">SUPPORTED CONTEXT</span>
          <h2 id="context-title">Choose a conversation setting</h2>
        </div>
        <div className="mode-grid">
          <HospitalMode active={context === "hospital"} onSelect={setContext} />
          <BankMode active={context === "bank"} onSelect={setContext} />
          <OfficeMode active={context === "office"} onSelect={setContext} />
        </div>
        <p className="context-note">
          Active context: <strong>{context}</strong>. It limits future glosses;
          it does not enable model inference in this foundation.
        </p>
      </section>

      <section className="conversation-layout">
        <SignInputPanel />

        <section className="panel conversation-panel" aria-labelledby="state-title">
          <TurnIndicator turn={state.turn} />
          <div className="panel-header state-header">
            <div>
              <span className="panel-kicker">LOCAL SESSION</span>
              <h2 id="state-title">Conversation state</h2>
            </div>
            <button
              type="button"
              className="button secondary"
              onClick={conversationStore.clear}
              disabled={!state.messages.length && !state.glosses.length}
            >
              Clear session
            </button>
          </div>

          <div className="gloss-list" aria-label="Current glosses">
            {state.glosses.length ? (
              state.glosses.map((gloss) => <GlossChip key={gloss} gloss={gloss} />)
            ) : (
              <span className="muted-state">No glosses recognized yet.</span>
            )}
          </div>

          <Transcript messages={state.messages} />
          <p className="foundation-notice">
            This session is local UI state. No transcript is fabricated from
            microphone audio, and no sign prediction is claimed.
          </p>
        </section>
      </section>
    </main>
  );
}

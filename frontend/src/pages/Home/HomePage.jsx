import React, { useState } from "react";

import MicButton from "../../features/speech-input/components/MicButton";
import AudioStatus from "../../features/speech-input/components/AudioStatus";
import useMicrophone from "../../features/speech-input/hooks/useMicrophone";

import SignAvatar from "../../features/avatar/components/SignAvatar";
import AvatarControls from "../../features/avatar/components/AvatarControls";

export default function HomePage() {
  const microphone = useMicrophone();
  const [gesture, setGesture] = useState("idle");

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">VOXIS / SILENTSIGN</span>

          <h1>
            Speech
            <span> → </span>
            Sign
          </h1>

          <p>
            Phase 1 foundation for the Rishi pipeline:
            microphone capture + 3D avatar runtime.
          </p>
        </div>

        <div className="phase-card">
          <span>ACTIVE PHASE</span>
          <strong>01</strong>
          <small>Input Foundation</small>
        </div>
      </section>

      <section className="workspace">
        <section className="panel speech-panel">
          <div className="panel-header">
            <div>
              <span className="panel-kicker">RISHI / SPEECH INPUT</span>
              <h2>Microphone</h2>
            </div>

            <AudioStatus
              status={microphone.status}
              error={microphone.error}
            />
          </div>

          <div className="mic-workspace">
            <MicButton
              isRecording={microphone.isRecording}
              disabled={!microphone.isSupported}
              onStart={microphone.startRecording}
              onStop={microphone.stopRecording}
            />

            <div className="recording-info">
              <strong>{microphone.durationLabel}</strong>

              <span>
                {microphone.isSupported
                  ? microphone.isRecording
                    ? "Listening..."
                    : "Microphone ready"
                  : "Microphone unavailable"}
              </span>
            </div>
          </div>

          {microphone.audioUrl && (
            <div className="recording-result">
              <div>
                <span className="panel-kicker">CAPTURED AUDIO</span>

                <strong>
                  {(microphone.audioBlob?.size || 0).toLocaleString()} bytes
                </strong>
              </div>

              <audio controls src={microphone.audioUrl} />

              <small>
                Phase 1 complete target: audio Blob successfully captured.
                Whisper starts in Phase 2.
              </small>
            </div>
          )}
        </section>

        <section className="panel avatar-panel">
          <div className="panel-header">
            <div>
              <span className="panel-kicker">RISHI / AVATAR</span>
              <h2>3D Sign Avatar</h2>
            </div>

            <span className="status-pill success">ONLINE</span>
          </div>

          <div className="avatar-stage">
            <SignAvatar gesture={gesture} />
          </div>

          <AvatarControls
            gesture={gesture}
            onGestureChange={setGesture}
          />
        </section>
      </section>

      <section className="architecture-strip">
        <div>
          <span>01</span>
          <strong>Microphone</strong>
          <small>Browser audio capture</small>
        </div>

        <div>
          <span>02</span>
          <strong>Whisper</strong>
          <small>Phase 2</small>
        </div>

        <div>
          <span>03</span>
          <strong>Text → Gloss</strong>
          <small>Phase 3</small>
        </div>

        <div>
          <span>04</span>
          <strong>Gloss → Avatar</strong>
          <small>Phase 4</small>
        </div>
      </section>
    </main>
  );
}

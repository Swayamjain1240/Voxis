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
          <span className="eyebrow">VOXIS / ISL COMMUNICATION</span>

          <h1>
            Speech
            <span> → </span>
            Sign
          </h1>

          <p>
            Phase 2 speech preparation: bounded microphone capture with an
            optional local Whisper transcription runtime.
          </p>
        </div>

        <div className="phase-card">
          <span>ACTIVE PHASE</span>
          <strong>02</strong>
          <small>Data &amp; Speech Preparation</small>
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

              <button
                type="button"
                className="button secondary"
                onClick={microphone.uploadAudio}
                disabled={microphone.uploadStatus === "uploading"}
              >
                {microphone.uploadStatus === "uploading"
                  ? "Checking upload..."
                  : "Validate upload"}
              </button>

              <button
                type="button"
                className="button secondary"
                onClick={microphone.transcribeAudio}
                disabled={microphone.transcriptionStatus === "transcribing"}
              >
                {microphone.transcriptionStatus === "transcribing"
                  ? "Transcribing..."
                  : microphone.transcriptionStatus === "error"
                    ? "Retry transcription"
                    : "Transcribe speech"}
              </button>

              {microphone.uploadStatus === "uploaded" && (
                <p className="foundation-success">
                  Audio passed the bounded backend upload boundary. Whisper is
                  still disabled, so no transcript was generated.
                </p>
              )}
              {microphone.uploadError && (
                <p className="foundation-error">{microphone.uploadError}</p>
              )}

              {microphone.transcriptionResult?.transcript && (
                <div className="transcription-result" aria-live="polite">
                  <span className="panel-kicker">TRANSCRIPT / ENGLISH</span>
                  <p>{microphone.transcriptionResult.transcript}</p>
                  {microphone.transcriptionResult.confidence != null && (
                    <small>
                      Confidence: {Math.round(microphone.transcriptionResult.confidence * 100)}%
                    </small>
                  )}
                </div>
              )}
              {microphone.transcriptionError && (
                <p className="foundation-error" role="alert">
                  {microphone.transcriptionError}
                </p>
              )}

              <small>
                Capture is local until you choose to validate the upload.
                 Uploading does not start transcription. Transcription uses the
                 optional local Whisper runtime when enabled.
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

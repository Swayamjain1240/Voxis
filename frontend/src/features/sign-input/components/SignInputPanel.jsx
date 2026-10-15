import React from "react";

import useSignCapture from "../hooks/useSignCapture";
import CameraFeed from "./CameraFeed";
import LandmarkOverlay from "./LandmarkOverlay";
import SignStatus from "./SignStatus";
import { downloadSequence } from "../services/sequenceExport";

export default function SignInputPanel() {
  const capture = useSignCapture();
  const { camera, mediaPipe } = capture;
  const isActive = camera.isActive;
  const [downloadStatus, setDownloadStatus] = React.useState("");

  const handleDownload = () => {
    try {
      const filename = downloadSequence(capture.sequence);
      setDownloadStatus(`Downloaded ${filename}`);
    } catch (downloadError) {
      setDownloadStatus(
        downloadError?.message || "The sequence could not be downloaded."
      );
    }
  };

  return (
    <section className="panel sign-input-panel" aria-labelledby="sign-input-title">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">MODE 1 / SIGN INPUT</span>
          <h2 id="sign-input-title">Camera foundation</h2>
        </div>
        <SignStatus status={capture.captureStatus} />
      </div>

      <div className="camera-stage" aria-live="polite">
        {isActive ? (
          <>
            <CameraFeed ref={capture.videoRef} stream={camera.stream} />
            <LandmarkOverlay landmarks={mediaPipe.landmarks} />
          </>
        ) : (
          <div className="camera-empty">
            <strong>Camera is off</strong>
            <span>Start camera to request permission and show local video.</span>
          </div>
        )}
      </div>

      <div className="capture-controls">
        <button
          type="button"
          className="button primary"
          onClick={isActive ? capture.stop : capture.start}
        >
          {isActive ? "Stop camera" : "Start camera"}
        </button>
        <button
          type="button"
          className="button secondary"
          onClick={capture.clearSequence}
          disabled={!capture.frameCount}
        >
          Clear frames
        </button>
        <button
          type="button"
          className="button secondary"
          onClick={handleDownload}
          disabled={!capture.sequence}
        >
          Download sequence
        </button>
      </div>

      <div className="capture-meta">
        <span>Frames: {capture.frameCount}/60</span>
        <span>MediaPipe: {mediaPipe.status}</span>
      </div>

      {camera.error && <p className="foundation-error">{camera.error}</p>}
      {mediaPipe.error && <p className="foundation-notice">{mediaPipe.error}</p>}
      {capture.captureError && (
        <p className="foundation-error">{capture.captureError}</p>
      )}
      {downloadStatus && (
        <p className="foundation-notice" role="status">
          {downloadStatus}
        </p>
      )}
      {capture.sequence && (
        <p className="foundation-success">
          A complete 60-frame sequence is buffered locally and ready to
          download. Sign prediction is not enabled in Phase 1.
        </p>
      )}
    </section>
  );
}

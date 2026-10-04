import React from "react";

export default function MicButton({
  isRecording,
  disabled,
  onStart,
  onStop,
}) {
  const handleClick = () => {
    if (isRecording) {
      onStop?.();
    } else {
      onStart?.();
    }
  };

  return (
    <button
      type="button"
      className={`mic-button ${isRecording ? "recording" : ""}`}
      disabled={disabled}
      onClick={handleClick}
      aria-label={isRecording ? "Stop recording" : "Start recording"}
      aria-pressed={isRecording}
    >
      <span className="mic-button-icon">
        {isRecording ? "■" : "🎙"}
      </span>

      <span className="mic-button-label">
        {isRecording ? "Stop recording" : "Start microphone"}
      </span>
    </button>
  );
}

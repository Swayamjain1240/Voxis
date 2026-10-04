import React from "react";

const STATUS_LABELS = {
  idle: "READY",
  requesting: "REQUESTING",
  recording: "RECORDING",
  stopped: "RECORDED",
  error: "ERROR",
};

export default function AudioStatus({ status = "idle", error = "" }) {
  const label = STATUS_LABELS[status] || "READY";

  return (
    <span
      className={`status-pill ${
        status === "error"
          ? "danger"
          : status === "recording"
            ? "active"
            : ""
      }`}
      title={error || label}
    >
      <span className="status-dot" />
      {label}
    </span>
  );
}

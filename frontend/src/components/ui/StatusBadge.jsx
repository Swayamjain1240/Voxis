import React from "react";

export default function StatusBadge({
  children,
  tone = "success",
}) {
  return (
    <span className={`status-pill ${tone}`}>
      <span className="status-dot" />
      {children}
    </span>
  );
}

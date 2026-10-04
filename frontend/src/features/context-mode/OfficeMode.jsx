import React from "react";

export default function OfficeMode({
  active,
  onSelect,
}) {
  return (
    <button
      type="button"
      className={`mode-card ${
        active ? "active" : ""
      }`}
      onClick={() => onSelect?.("office")}
    >
      <strong>Office</strong>
      <span>
        HELP · YES · NO · YESTERDAY
      </span>
    </button>
  );
}

import React from "react";

export default function HospitalMode({
  active,
  onSelect,
}) {
  return (
    <button
      type="button"
      className={`mode-card ${
        active ? "active" : ""
      }`}
      onClick={() => onSelect?.("hospital")}
    >
      <strong>Hospital</strong>
      <span>
        DOCTOR · MEDICINE · PAIN · HELP
      </span>
    </button>
  );
}

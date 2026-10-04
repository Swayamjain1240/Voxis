import React from "react";

export default function BankMode({
  active,
  onSelect,
}) {
  return (
    <button
      type="button"
      className={`mode-card ${
        active ? "active" : ""
      }`}
      onClick={() => onSelect?.("bank")}
    >
      <strong>Bank</strong>
      <span>
        BANK · MONEY · WHERE · YES · NO
      </span>
    </button>
  );
}

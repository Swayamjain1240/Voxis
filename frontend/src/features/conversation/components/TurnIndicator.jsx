import React from "react";

export default function TurnIndicator({
  turn = "speech",
}) {
  const label =
    turn === "speech"
      ? "Speech / Hearing side"
      : "Sign / Deaf side";

  return (
    <div className="turn-indicator">
      <span>ACTIVE TURN</span>
      <strong>{label}</strong>
    </div>
  );
}

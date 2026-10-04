import React from "react";

const CONTROLS = [
  {
    id: "idle",
    label: "Idle",
  },
  {
    id: "wave",
    label: "Wave",
  },
  {
    id: "sign",
    label: "Sign Demo",
  },
];

export default function AvatarControls({
  gesture,
  onGestureChange,
}) {
  return (
    <div className="avatar-controls">
      {CONTROLS.map((control) => (
        <button
          key={control.id}
          type="button"
          className={`button ${
            gesture === control.id ? "primary" : "secondary"
          }`}
          onClick={() => onGestureChange(control.id)}
        >
          {control.label}
        </button>
      ))}
    </div>
  );
}

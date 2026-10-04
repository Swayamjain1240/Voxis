import React from "react";

export default function Button({
  children,
  variant = "primary",
  ...props
}) {
  return (
    <button
      type="button"
      className={`button ${variant}`}
      {...props}
    >
      {children}
    </button>
  );
}

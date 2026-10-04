import React from "react";
import { NavLink } from "react-router-dom";

export default function AppShell({
  children,
}) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <NavLink
          to="/"
          className="brand"
        >
          <span className="brand-mark">
            V
          </span>

          <span className="brand-text">
            <strong>VOXIS</strong>
            <small>SilentSign</small>
          </span>
        </NavLink>

        <nav className="main-nav">
          <NavLink
            to="/"
            end
          >
            Home
          </NavLink>

          <NavLink to="/conversation">
            Conversation
          </NavLink>

          <NavLink to="/debug">
            Debug
          </NavLink>
        </nav>

        <div className="system-status">
          <span className="system-dot" />
          MODE 1
        </div>
      </header>

      {children}
    </div>
  );
}

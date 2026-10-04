import React from "react";

/*
 * Application-wide providers belong here.
 *
 * Future providers:
 * - global state
 * - query client
 * - telemetry
 * - authentication, if ever required
 *
 * Mode 1 currently needs no authentication.
 */
export function AppProviders({ children }) {
  return children;
}

import { describe, expect, it } from "vitest";

import { cameraErrorMessage } from "../src/features/sign-input/hooks/useCamera.js";

describe("camera permission boundary", () => {
  it("turns browser camera failures into actionable messages", () => {
    expect(cameraErrorMessage({ name: "NotAllowedError" })).toMatch(/denied/i);
    expect(cameraErrorMessage({ name: "NotFoundError" })).toMatch(/found/i);
    expect(cameraErrorMessage({ name: "NotReadableError" })).toMatch(/busy/i);
    expect(cameraErrorMessage({ message: "camera failed" })).toBe("camera failed");
  });
});

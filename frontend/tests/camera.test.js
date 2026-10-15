import { describe, expect, it } from "vitest";

import { cameraErrorMessage } from "../src/features/sign-input/hooks/useCamera.js";
import { isVideoReadyForCapture } from "../src/features/sign-input/hooks/useSignCapture.js";

describe("camera permission boundary", () => {
  it("turns browser camera failures into actionable messages", () => {
    expect(cameraErrorMessage({ name: "NotAllowedError" })).toMatch(/denied/i);
    expect(cameraErrorMessage({ name: "NotFoundError" })).toMatch(/found/i);
    expect(cameraErrorMessage({ name: "NotReadableError" })).toMatch(/busy/i);
    expect(cameraErrorMessage({ message: "camera failed" })).toBe("camera failed");
  });

  it("waits for a video element to have real dimensions before processing", () => {
    expect(
      isVideoReadyForCapture({ readyState: 1, videoWidth: 1280, videoHeight: 720 })
    ).toBe(false);
    expect(
      isVideoReadyForCapture({ readyState: 2, videoWidth: 1280, videoHeight: 720 })
    ).toBe(true);
    expect(
      isVideoReadyForCapture({ readyState: 2, videoWidth: 0, videoHeight: 720 })
    ).toBe(false);
  });
});

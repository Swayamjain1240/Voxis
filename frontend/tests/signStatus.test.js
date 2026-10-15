import { describe, expect, it } from "vitest";

import { formatSignStatus } from "../src/features/sign-input/components/SignStatus.jsx";

describe("sign capture status labels", () => {
  it("turns internal states into user-facing messages", () => {
    expect(formatSignStatus("camera_loading")).toBe("Camera loading");
    expect(formatSignStatus("no_detection")).toBe("No landmarks detected");
    expect(formatSignStatus("sequence_ready")).toBe("Sequence ready");
  });

  it("keeps unknown states visible instead of hiding them", () => {
    expect(formatSignStatus("future_state")).toBe("future_state");
  });
});

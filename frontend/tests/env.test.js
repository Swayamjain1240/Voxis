import { describe, expect, it } from "vitest";

import { frontendConfig, mediaPipeConfig } from "../src/config/env.js";

describe("frontend environment boundary", () => {
  it("uses public defaults without requiring credentials", () => {
    expect(frontendConfig.appName).toBe("VOXIS");
    expect(frontendConfig.apiBaseUrl).toContain("/api/v1");
    expect(mediaPipeConfig.configured).toBe(false);
  });
});

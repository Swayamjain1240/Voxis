import { describe, expect, it } from "vitest";

import {
  APP_NAME,
  APP_PHASE,
  MAX_SIGN_SEQUENCE_LENGTH,
} from "../src/constants/app";

describe("VOXIS frontend foundation", () => {
  it("has the correct application identity", () => {
    expect(APP_NAME).toBe("VOXIS");
  });

  it("starts from Phase 1", () => {
    expect(APP_PHASE).toBe(1);
  });

  it("uses a bounded sign sequence length", () => {
    expect(
      MAX_SIGN_SEQUENCE_LENGTH
    ).toBe(60);
  });
});

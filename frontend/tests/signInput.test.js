import { describe, expect, it } from "vitest";

import {
  FEATURES_PER_FRAME,
  TOTAL_LANDMARK_COUNT,
  canonicalizeLandmarks,
  flattenCanonicalFrame,
  hasDetectedLandmarks,
} from "../src/features/sign-input/services/landmarkExtractor.js";
import { FrameBuffer } from "../src/features/sign-input/services/frameBuffer.js";
import {
  isCanonicalSequence,
  sequenceProgress,
} from "../src/features/sign-input/services/sequence.js";

function frame(value = 0) {
  return Array.from({ length: FEATURES_PER_FRAME }, () => value);
}

describe("canonical sign input contract", () => {
  it("pads MediaPipe results to 75 landmarks and 300 finite features", () => {
    const result = {
      leftHandLandmarks: [{ x: 1, y: 2, z: 3 }],
      poseLandmarks: [{ x: 4, y: 5, z: 6, visibility: 0.8 }],
    };

    const landmarks = canonicalizeLandmarks(result);
    const flattened = flattenCanonicalFrame(result);

    expect(landmarks).toHaveLength(TOTAL_LANDMARK_COUNT);
    expect(flattened).toHaveLength(FEATURES_PER_FRAME);
    expect(flattened.every(Number.isFinite)).toBe(true);
    expect(flattened.slice(0, 4)).toEqual([1, 2, 3, 1]);
    expect(flattened.slice(84, 88)).toEqual([0, 0, 0, 0]);
    expect(hasDetectedLandmarks(result)).toBe(true);
  });

  it("reports an empty MediaPipe result without inventing detection", () => {
    expect(hasDetectedLandmarks({})).toBe(false);
  });
});

describe("bounded sign frame buffer", () => {
  it("returns no sequence before full and keeps only the latest frames", () => {
    const buffer = new FrameBuffer(3);

    buffer.push(frame(1));
    buffer.push(frame(2));
    expect(buffer.sequence()).toBeNull();

    buffer.push(frame(3));
    buffer.push(frame(4));

    expect(buffer.isFull()).toBe(true);
    expect(buffer.values().map((item) => item[0])).toEqual([2, 3, 4]);
  });

  it("rejects invalid feature dimensions and non-finite values", () => {
    const buffer = new FrameBuffer();

    expect(() => buffer.push([])).toThrow(/300 finite features/);
    expect(() => buffer.push(frame(Number.NaN))).toThrow(/300 finite features/);
    expect(() => new FrameBuffer(61)).toThrow(/between 1 and 60/);
  });
});

describe("canonical sequence contract", () => {
  it("accepts only a complete sequence of canonical frames", () => {
    expect(isCanonicalSequence(Array.from({ length: 60 }, () => frame(1)))).toBe(true);
    expect(isCanonicalSequence(Array.from({ length: 59 }, () => frame(1)))).toBe(false);
    expect(isCanonicalSequence(Array.from({ length: 60 }, () => frame(Number.NaN)))).toBe(false);
  });

  it("reports bounded capture progress", () => {
    expect(sequenceProgress(12)).toEqual({
      count: 12,
      max: 60,
      ratio: 0.2,
      ready: false,
    });
    expect(sequenceProgress(100, 3).ready).toBe(true);
  });
});

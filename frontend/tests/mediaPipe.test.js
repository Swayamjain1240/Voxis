import { describe, expect, it } from "vitest";

import {
  createProcessorOptions,
  mapHolisticResult,
} from "../src/features/sign-input/hooks/useMediaPipe.js";

describe("MediaPipe adapter", () => {
  it("maps Tasks Vision nested results into the app boundary", () => {
    const result = mapHolisticResult({
      leftHandLandmarks: [[{ x: 1 }]],
      rightHandLandmarks: [[{ x: 2 }]],
      poseLandmarks: [[{ x: 3 }]],
    });

    expect(result.leftHandLandmarks[0].x).toBe(1);
    expect(result.rightHandLandmarks[0].x).toBe(2);
    expect(result.poseLandmarks[0].x).toBe(3);
  });

  it("keeps local model and WASM paths in the processor options", () => {
    const options = createProcessorOptions({
      modelAssetPath: "/models/holistic.task",
      wasmRoot: "/mediapipe/wasm",
    });

    expect(options.baseOptions.modelAssetPath).toBe("/models/holistic.task");
    expect(options.runningMode).toBe("VIDEO");
  });
});

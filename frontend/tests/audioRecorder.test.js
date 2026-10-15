import { afterEach, describe, expect, it, vi } from "vitest";

import {
  createAudioRecorder,
  getSupportedMimeType,
} from "../src/features/speech-input/services/audioRecorder.js";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("local audio recorder boundary", () => {
  it("selects a browser-supported type and emits one bounded blob", () => {
    class FakeMediaRecorder {
      static isTypeSupported(type) {
        return type === "audio/ogg;codecs=opus";
      }

      constructor() {
        this.mimeType = "audio/ogg;codecs=opus";
        this.state = "inactive";
        this.listeners = {};
      }

      addEventListener(name, callback) {
        this.listeners[name] = callback;
      }

      start() {
        this.state = "recording";
        this.listeners.start?.();
      }

      stop() {
        this.state = "inactive";
        this.listeners.dataavailable?.({ data: new Blob(["audio"]) });
        this.listeners.stop?.();
      }
    }

    vi.stubGlobal("MediaRecorder", FakeMediaRecorder);
    expect(getSupportedMimeType()).toBe("audio/ogg;codecs=opus");

    const onStop = vi.fn();
    const recorder = createAudioRecorder({
      stream: { getTracks: () => [] },
      mimeType: getSupportedMimeType(),
      onStop,
    });
    recorder.start();
    recorder.stop();

    expect(onStop).toHaveBeenCalledOnce();
    expect(onStop.mock.calls[0][0].type).toBe("audio/ogg;codecs=opus");
    expect(onStop.mock.calls[0][0].size).toBeGreaterThan(0);
  });
});

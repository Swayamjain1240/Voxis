import { afterEach, describe, expect, it, vi } from "vitest";
import {
  audioFilenameForBlob,
  getHealth,
  textToGloss,
  uploadSpeechAudio,
} from "../src/services/api.js";

afterEach(() => vi.unstubAllGlobals());

describe("REST contract adapter", () => {
  it("uses the actual recorded audio type for bounded uploads", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      data: { accepted: true },
      meta: { api_version: "v1", schema_version: "1.0.0", request_id: "req" },
    }), { headers: { "content-type": "application/json" } }));
    vi.stubGlobal("fetch", fetchMock);
    const blob = new Blob(["audio"], { type: "audio/ogg;codecs=opus" });

    expect(audioFilenameForBlob(blob)).toBe("speech.ogg");
    await uploadSpeechAudio(blob);
    const body = fetchMock.mock.calls[0][1].body;
    expect(body.get("audio").name).toBe("speech.ogg");
    expect(body.get("audio").type).toBe("audio/ogg;codecs=opus");
  });

  it("unwraps the canonical envelope while keeping caller data stable", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true, data: { glosses: ["HELP"] },
      meta: { api_version: "v1", schema_version: "1.0.0", request_id: "req" },
    }), { headers: { "content-type": "application/json" } }));
    vi.stubGlobal("fetch", fetchMock);
    expect(await textToGloss("help", "hospital")).toEqual({ glosses: ["HELP"] });
    const [url, options] = fetchMock.mock.calls[0];
    expect(url).not.toContain("help");
    expect(JSON.parse(options.body)).toEqual({ text: "help", context: "hospital" });
    expect(options.credentials).toBe("omit");
    expect(options.signal).toBeInstanceOf(AbortSignal);
  });

  it("surfaces safe unavailable-service errors and request IDs", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: false, error: { code: "WHISPER_UNAVAILABLE", message: "Service unavailable." },
      meta: { request_id: "req-1" },
    }), { status: 503, headers: { "content-type": "application/json" } })));
    await expect(getHealth()).rejects.toMatchObject({
      message: "Service unavailable.", code: "WHISPER_UNAVAILABLE", requestId: "req-1",
    });
  });

  it("rejects unexpected successful response shapes", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("{}", {
      headers: { "content-type": "application/json" },
    })));
    await expect(getHealth()).rejects.toThrow("unsupported response contract");
  });
});

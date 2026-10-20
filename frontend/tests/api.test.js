import { afterEach, describe, expect, it, vi } from "vitest";
import {
  audioFilenameForBlob,
  getHealth,
  textToGloss,
  transcribeSpeech,
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

  it("posts the recorded blob to the transcription endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      success: true,
      data: { transcript: "Where does it hurt?", language: "en" },
      meta: { api_version: "v1", schema_version: "1.0.0", request_id: "req" },
    }), { headers: { "content-type": "application/json" } }));
    vi.stubGlobal("fetch", fetchMock);
    const result = await transcribeSpeech(
      new Blob(["audio"], { type: "audio/ogg;codecs=opus" })
    );

    expect(result.transcript).toBe("Where does it hurt?");
    expect(fetchMock.mock.calls[0][0]).toContain("/speech/transcribe");
    expect(fetchMock.mock.calls[0][1].body.get("audio").name).toBe("speech.ogg");
  });
});

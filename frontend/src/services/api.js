import { frontendConfig } from "../config/env.js";

const API_BASE_URL = frontendConfig.apiBaseUrl;

async function request(
  path,
  options = {}
) {
  const headers = {
    ...(options.body instanceof FormData
      ? {}
      : {
          "Content-Type":
            "application/json",
        }),
    ...(options.headers || {}),
  };

  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,
      headers,
      signal: options.signal || AbortSignal.timeout(15000),
      credentials: "omit",
    }
  );

  const contentType =
    response.headers.get(
      "content-type"
    ) || "";

  const payload =
    contentType.includes(
      "application/json"
    )
      ? await response.json()
      : await response.text();

  if (!response.ok) {
    const message = payload?.error?.message ||
      (typeof payload?.detail === "string" ? payload.detail :
        `Request failed with status ${response.status}`);
    const error = new Error(message);
    error.code = payload?.error?.code || "REQUEST_ERROR";
    error.requestId = payload?.meta?.request_id;
    throw error;
  }

  if (payload?.success !== true || payload?.meta?.api_version !== "v1" ||
      payload?.meta?.schema_version !== "1.0.0" || !("data" in payload)) {
    throw new Error("The server returned an unsupported response contract.");
  }
  return payload.data;
}

export function getHealth() {
  return request("/health");
}

export function getSpeechCapabilities() {
  return request(
    "/speech/capabilities"
  );
}

export function uploadSpeechAudio(
  audioBlob
) {
  const formData = new FormData();

  formData.append(
    "audio",
    audioBlob,
    "speech.webm"
  );

  return request("/speech/upload", {
    method: "POST",
    body: formData,
  });
}

export function transcribeSpeech(
  audioBlob
) {
  const formData = new FormData();

  formData.append(
    "audio",
    audioBlob,
    "speech.webm"
  );

  return request(
    "/speech/transcribe",
    {
      method: "POST",
      body: formData,
    }
  );
}

export function postConversationMessage(message) {
  return request("/conversation/message", { method: "POST", body: JSON.stringify(message) });
}

export function textToGloss(text, context = null) {
  return request("/conversation/text-to-gloss", {
    method: "POST", body: JSON.stringify({ text, context }),
  });
}

export function glossToText(glosses, context = null) {
  return request("/conversation/gloss-to-text", {
    method: "POST", body: JSON.stringify({ glosses, context }),
  });
}

export { API_BASE_URL };

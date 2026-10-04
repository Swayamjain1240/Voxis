const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api/v1";

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
    const message =
      typeof payload === "object" &&
      payload?.detail
        ? payload.detail
        : `Request failed with status ${response.status}`;

    throw new Error(message);
  }

  return payload;
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

export { API_BASE_URL };

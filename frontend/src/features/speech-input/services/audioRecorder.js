export const AUDIO_MIME_TYPES = [
  "audio/webm;codecs=opus",
  "audio/webm",
  "audio/ogg;codecs=opus",
  "audio/mp4",
];

export function getSupportedMimeType() {
  if (typeof MediaRecorder === "undefined") {
    return "";
  }

  return (
    AUDIO_MIME_TYPES.find((type) =>
      MediaRecorder.isTypeSupported(type)
    ) || ""
  );
}

export function createAudioRecorder({
  stream,
  mimeType = "",
  onStart,
  onStop,
  onError,
}) {
  if (!stream) {
    throw new Error("A MediaStream is required.");
  }

  const recorder = mimeType
    ? new MediaRecorder(stream, { mimeType })
    : new MediaRecorder(stream);

  const chunks = [];

  recorder.addEventListener("start", () => {
    onStart?.();
  });

  recorder.addEventListener("dataavailable", (event) => {
    if (event.data && event.data.size > 0) {
      chunks.push(event.data);
    }
  });

  recorder.addEventListener("stop", () => {
    const type = recorder.mimeType || mimeType || "audio/webm";

    onStop?.(
      new Blob(chunks, {
        type,
      })
    );
  });

  recorder.addEventListener("error", (event) => {
    onError?.(
      event.error || new Error("MediaRecorder encountered an error.")
    );
  });

  return recorder;
}

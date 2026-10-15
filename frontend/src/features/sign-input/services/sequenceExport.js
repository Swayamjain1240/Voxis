import { FEATURES_PER_FRAME } from "./landmarkExtractor.js";
import {
  isCanonicalSequence,
  MAX_SIGN_SEQUENCE_LENGTH,
} from "./sequence.js";

export const SEQUENCE_SCHEMA_VERSION = "1.0.0";

export function serializeSequence(
  sequence,
  {
    capturedAt = new Date().toISOString(),
    source = "browser-camera",
  } = {}
) {
  if (!isCanonicalSequence(sequence)) {
    throw new Error(
      `Only a complete ${MAX_SIGN_SEQUENCE_LENGTH}-frame canonical sequence can be exported.`
    );
  }

  return JSON.stringify(
    {
      schema_version: SEQUENCE_SCHEMA_VERSION,
      sequence_length: MAX_SIGN_SEQUENCE_LENGTH,
      features_per_frame: FEATURES_PER_FRAME,
      captured_at: capturedAt,
      source,
      frames: sequence,
    },
    null,
    2
  );
}

export function downloadSequence(
  sequence,
  {
    filename = `voxis-sign-sequence-${Date.now()}.json`,
    documentRef = globalThis.document,
    urlRef = globalThis.URL,
  } = {}
) {
  const payload = serializeSequence(sequence);

  if (!documentRef?.createElement || !urlRef?.createObjectURL) {
    throw new Error("Local sequence download is not supported in this browser.");
  }

  const blob = new Blob([payload], { type: "application/json" });
  const url = urlRef.createObjectURL(blob);
  const link = documentRef.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  urlRef.revokeObjectURL?.(url);
  return filename;
}

import { MAX_SIGN_SEQUENCE_LENGTH } from "../../../constants/app.js";
import { isCanonicalFrame } from "./landmarkExtractor.js";

export { MAX_SIGN_SEQUENCE_LENGTH };

export function isCanonicalSequence(
  sequence,
  expectedLength = MAX_SIGN_SEQUENCE_LENGTH
) {
  return (
    Array.isArray(sequence) &&
    sequence.length === expectedLength &&
    sequence.every(isCanonicalFrame)
  );
}

export function sequenceProgress(
  frameCount,
  maxLength = MAX_SIGN_SEQUENCE_LENGTH
) {
  const safeMax = Math.max(1, Math.floor(Number(maxLength) || 1));
  const safeCount = Math.max(0, Math.min(safeMax, Math.floor(Number(frameCount) || 0)));

  return {
    count: safeCount,
    max: safeMax,
    ratio: safeCount / safeMax,
    ready: safeCount >= safeMax,
  };
}

import {
  isCanonicalFrame,
  FEATURES_PER_FRAME,
} from "./landmarkExtractor";
import { MAX_SIGN_SEQUENCE_LENGTH } from "../../../constants/app.js";

export { MAX_SIGN_SEQUENCE_LENGTH };

export class FrameBuffer {
  constructor(maxLength = MAX_SIGN_SEQUENCE_LENGTH) {
    if (
      !Number.isInteger(maxLength) ||
      maxLength <= 0 ||
      maxLength > MAX_SIGN_SEQUENCE_LENGTH
    ) {
      throw new Error(
        `FrameBuffer maxLength must be an integer between 1 and ${MAX_SIGN_SEQUENCE_LENGTH}.`
      );
    }

    this.maxLength = maxLength;
    this.frames = [];
  }

  push(frame) {
    if (!isCanonicalFrame(frame)) {
      throw new Error(
        `FrameBuffer frames must contain exactly ${FEATURES_PER_FRAME} finite features.`
      );
    }

    this.frames.push([...frame]);

    while (this.frames.length > this.maxLength) {
      this.frames.shift();
    }

    return this.frames.length;
  }

  clear() {
    this.frames = [];
  }

  isFull() {
    return this.frames.length >= this.maxLength;
  }

  size() {
    return this.frames.length;
  }

  values() {
    return this.frames.map((frame) => [...frame]);
  }

  sequence() {
    return this.isFull() ? this.values() : null;
  }
}

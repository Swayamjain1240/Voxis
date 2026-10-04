export class FrameBuffer {
  constructor(maxLength = 60) {
    if (!Number.isInteger(maxLength) || maxLength <= 0) {
      throw new Error(
        "FrameBuffer maxLength must be a positive integer."
      );
    }

    this.maxLength = maxLength;
    this.frames = [];
  }

  push(frame) {
    this.frames.push(frame);

    while (
      this.frames.length >
      this.maxLength
    ) {
      this.frames.shift();
    }

    return this.frames.length;
  }

  clear() {
    this.frames = [];
  }

  isFull() {
    return (
      this.frames.length >=
      this.maxLength
    );
  }

  size() {
    return this.frames.length;
  }

  values() {
    return [...this.frames];
  }
}

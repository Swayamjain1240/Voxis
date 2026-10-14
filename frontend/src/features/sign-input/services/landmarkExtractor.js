export const LEFT_HAND_LANDMARK_COUNT = 21;
export const RIGHT_HAND_LANDMARK_COUNT = 21;
export const POSE_LANDMARK_COUNT = 33;
export const TOTAL_LANDMARK_COUNT =
  LEFT_HAND_LANDMARK_COUNT +
  RIGHT_HAND_LANDMARK_COUNT +
  POSE_LANDMARK_COUNT;
export const FEATURES_PER_LANDMARK = 4;
export const FEATURES_PER_FRAME =
  TOTAL_LANDMARK_COUNT * FEATURES_PER_LANDMARK;

function finiteOrZero(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : 0;
}

function toPoint(point, defaultVisibility = 1) {
  return {
    x: finiteOrZero(point?.x),
    y: finiteOrZero(point?.y),
    z: finiteOrZero(point?.z),
    visibility: Number.isFinite(Number(point?.visibility))
      ? Number(point.visibility)
      : defaultVisibility,
  };
}

function padLandmarks(landmarks, count) {
  return Array.from({ length: count }, (_, index) => {
    const point = landmarks?.[index];
    return point
      ? toPoint(point)
      : { x: 0, y: 0, z: 0, visibility: 0 };
  });
}

/**
 * Convert a MediaPipe result into the shared 75-point order:
 * left hand, right hand, then pose.
 */
export function canonicalizeLandmarks(result = {}) {
  return [
    ...padLandmarks(result.leftHandLandmarks, LEFT_HAND_LANDMARK_COUNT),
    ...padLandmarks(result.rightHandLandmarks, RIGHT_HAND_LANDMARK_COUNT),
    ...padLandmarks(result.poseLandmarks, POSE_LANDMARK_COUNT),
  ];
}

export function hasDetectedLandmarks(result = {}) {
  return Boolean(
    result.leftHandLandmarks?.length ||
      result.rightHandLandmarks?.length ||
      result.poseLandmarks?.length
  );
}

export function normalizeLandmarks(landmarks = []) {
  if (!landmarks.length) {
    return [];
  }

  const safeLandmarks = landmarks.map((point) => toPoint(point));
  const xs = safeLandmarks.map((point) => point.x);
  const ys = safeLandmarks.map((point) => point.y);

  const minX = Math.min(...xs);
  const minY = Math.min(...ys);
  const maxX = Math.max(...xs);
  const maxY = Math.max(...ys);
  const width = Math.max(maxX - minX, 1e-6);
  const height = Math.max(maxY - minY, 1e-6);

  return safeLandmarks.map((point) => ({
    ...point,
    x: (point.x - minX) / width,
    y: (point.y - minY) / height,
  }));
}

export function flattenLandmarks(landmarks = []) {
  return landmarks.flatMap((point) => {
    const safePoint = toPoint(point);
    return [
      safePoint.x,
      safePoint.y,
      safePoint.z,
      safePoint.visibility,
    ];
  });
}

export function flattenCanonicalFrame(resultOrLandmarks = {}) {
  const landmarks = Array.isArray(resultOrLandmarks)
    ? resultOrLandmarks
    : canonicalizeLandmarks(resultOrLandmarks);
  const frame = flattenLandmarks(landmarks);

  if (frame.length !== FEATURES_PER_FRAME || !isCanonicalFrame(frame)) {
    throw new Error(
      `Canonical sign frame must contain ${FEATURES_PER_FRAME} finite features.`
    );
  }

  return frame;
}

export function isCanonicalFrame(frame) {
  return (
    Array.isArray(frame) &&
    frame.length === FEATURES_PER_FRAME &&
    frame.every((value) => Number.isFinite(Number(value)))
  );
}

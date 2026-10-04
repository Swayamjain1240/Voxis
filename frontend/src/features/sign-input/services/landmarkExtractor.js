export function normalizeLandmarks(
  landmarks = []
) {
  if (!landmarks.length) {
    return [];
  }

  const xs = landmarks.map(
    (point) => Number(point?.x ?? 0)
  );

  const ys = landmarks.map(
    (point) => Number(point?.y ?? 0)
  );

  const minX = Math.min(...xs);
  const minY = Math.min(...ys);

  const maxX = Math.max(...xs);
  const maxY = Math.max(...ys);

  const width = Math.max(maxX - minX, 1e-6);
  const height = Math.max(maxY - minY, 1e-6);

  return landmarks.map((point) => ({
    x:
      (Number(point?.x ?? 0) - minX) /
      width,

    y:
      (Number(point?.y ?? 0) - minY) /
      height,

    z: Number(point?.z ?? 0),

    visibility: Number(
      point?.visibility ?? 1
    ),
  }));
}

export function flattenLandmarks(
  landmarks = []
) {
  return landmarks.flatMap((point) => [
    Number(point?.x ?? 0),
    Number(point?.y ?? 0),
    Number(point?.z ?? 0),
    Number(point?.visibility ?? 1),
  ]);
}

export function formatDuration(
  totalSeconds
) {
  const seconds = Math.max(
    0,
    Math.floor(totalSeconds)
  );

  const minutes = Math.floor(
    seconds / 60
  );

  const remaining =
    seconds % 60;

  return `${String(
    minutes
  ).padStart(2, "0")}:${String(
    remaining
  ).padStart(2, "0")}`;
}

export function findClip(clips = [], gloss) {
  const normalizedGloss = String(gloss).trim().toUpperCase();

  return (
    clips.find(
      (clip) =>
        String(clip?.name || "").toUpperCase() === normalizedGloss
    ) ||
    clips.find((clip) =>
      String(clip?.name || "")
        .toUpperCase()
        .includes(normalizedGloss)
    ) ||
    null
  );
}

export function createClipMap(clips = []) {
  return new Map(
    clips
      .filter((clip) => clip?.name)
      .map((clip) => [
        String(clip.name).toUpperCase(),
        clip,
      ])
  );
}

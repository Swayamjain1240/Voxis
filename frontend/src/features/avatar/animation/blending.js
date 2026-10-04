export function crossFade(
  previousAction,
  nextAction,
  duration = 0.2
) {
  if (!nextAction) {
    return;
  }

  nextAction.reset();
  nextAction.fadeIn(duration);
  nextAction.play();

  if (
    previousAction &&
    previousAction !== nextAction
  ) {
    previousAction.fadeOut(duration);
  }
}

export function stopWithFade(action, duration = 0.15) {
  if (!action) {
    return;
  }

  action.fadeOut(duration);
}

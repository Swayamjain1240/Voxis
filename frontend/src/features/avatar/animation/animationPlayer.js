import * as THREE from "three";

export class AnimationPlayer {
  constructor(rootObject) {
    if (!rootObject) {
      throw new Error("AnimationPlayer requires a root object.");
    }

    this.rootObject = rootObject;
    this.mixer = new THREE.AnimationMixer(rootObject);
    this.actions = new Map();
    this.activeAction = null;
  }

  registerClips(clips = []) {
    for (const clip of clips) {
      if (!clip?.name) {
        continue;
      }

      this.actions.set(
        clip.name.toUpperCase(),
        this.mixer.clipAction(clip)
      );
    }

    return this.actions;
  }

  play(name, options = {}) {
    const key = String(name).toUpperCase();
    const action = this.actions.get(key);

    if (!action) {
      return false;
    }

    const {
      fadeDuration = 0.2,
      loop = THREE.LoopOnce,
      clampWhenFinished = true,
    } = options;

    if (this.activeAction && this.activeAction !== action) {
      this.activeAction.fadeOut(fadeDuration);
    }

    action.reset();
    action.setLoop(loop);
    action.clampWhenFinished = clampWhenFinished;
    action.fadeIn(fadeDuration).play();

    this.activeAction = action;

    return true;
  }

  update(deltaSeconds) {
    this.mixer.update(deltaSeconds);
  }

  stopAll() {
    for (const action of this.actions.values()) {
      action.stop();
    }

    this.activeAction = null;
  }

  dispose() {
    this.stopAll();
    this.mixer.uncacheRoot(this.rootObject);
    this.actions.clear();
  }
}

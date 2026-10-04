const state = {
  mode: "mode-1",
  context: "hospital",
  debug: false,
};

const listeners = new Set();

function notify() {
  const snapshot = {
    ...state,
  };

  listeners.forEach(
    (listener) =>
      listener(snapshot)
  );
}

export const appStore = {
  getState() {
    return {
      ...state,
    };
  },

  subscribe(listener) {
    listeners.add(listener);

    return () =>
      listeners.delete(listener);
  },

  setMode(mode) {
    state.mode = mode;
    notify();
  },

  setContext(context) {
    state.context = context;
    notify();
  },

  setDebug(enabled) {
    state.debug = Boolean(enabled);
    notify();
  },
};

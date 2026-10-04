const state = {
  messages: [],
  glosses: [],
  turn: "speech",
};

const listeners = new Set();

function notify() {
  const snapshot = {
    ...state,
    messages: [...state.messages],
    glosses: [...state.glosses],
  };

  listeners.forEach((listener) =>
    listener(snapshot)
  );
}

export const conversationStore = {
  getState() {
    return {
      ...state,
      messages: [...state.messages],
      glosses: [...state.glosses],
    };
  },

  subscribe(listener) {
    listeners.add(listener);

    return () => {
      listeners.delete(listener);
    };
  },

  addMessage(message) {
    state.messages.push(message);
    notify();
  },

  setGlosses(glosses) {
    state.glosses = [...glosses];
    notify();
  },

  setTurn(turn) {
    state.turn = turn;
    notify();
  },

  clear() {
    state.messages = [];
    state.glosses = [];
    state.turn = "speech";
    notify();
  },
};

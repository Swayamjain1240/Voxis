import { beforeEach, describe, expect, it, vi } from "vitest";

import { conversationStore } from "../src/features/conversation/conversationStore.js";

beforeEach(() => conversationStore.clear());

describe("local conversation state", () => {
  it("publishes cloned state and resets all local data", () => {
    const listener = vi.fn();
    const unsubscribe = conversationStore.subscribe(listener);

    conversationStore.setTurn("sign");
    conversationStore.setGlosses(["PAIN"]);
    conversationStore.addMessage({
      message_id: "m-1",
      source: "sign",
      text: "Pending sign result",
    });

    const snapshot = conversationStore.getState();
    expect(snapshot.turn).toBe("sign");
    expect(snapshot.glosses).toEqual(["PAIN"]);
    expect(snapshot.messages).toHaveLength(1);
    expect(listener).toHaveBeenCalled();

    snapshot.messages.push({ message_id: "local-only" });
    expect(conversationStore.getState().messages).toHaveLength(1);

    conversationStore.clear();
    expect(conversationStore.getState()).toEqual({
      messages: [],
      glosses: [],
      turn: "speech",
    });
    unsubscribe();
  });
});

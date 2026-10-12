import { afterEach, describe, expect, it, vi } from "vitest";
import { createWebSocketClient } from "../src/services/websocket.js";

afterEach(() => vi.unstubAllGlobals());

describe("Mode 1 WebSocket boundary", () => {
  it("does not open a browser socket and reports the disabled transport", async () => {
    const WebSocketMock = vi.fn(() => {
      throw new Error("a browser socket must not be opened");
    });
    const onError = vi.fn();
    const onClose = vi.fn();
    vi.stubGlobal("WebSocket", WebSocketMock);

    const client = createWebSocketClient({ onError, onClose });

    expect(WebSocketMock).not.toHaveBeenCalled();
    expect(client.disabled).toBe(true);
    expect(client.readyState).toBe(3);
    expect(client.send({ type: "conversation.message" })).toBe(false);

    await Promise.resolve();
    expect(onError.mock.calls[0][0].code).toBe("WEBSOCKET_DISABLED");
    expect(onClose).toHaveBeenCalledWith({
      code: 1008,
      reason: "WebSocket transport is disabled in Mode 1.",
      wasClean: true,
    });
  });
});

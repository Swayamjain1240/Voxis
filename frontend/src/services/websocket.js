export function createWebSocketClient({
  onClose,
  onError,
} = {}) {
  const error = new Error("WebSocket transport is disabled in Mode 1.");
  error.code = "WEBSOCKET_DISABLED";
  const notify = globalThis.queueMicrotask || ((callback) => Promise.resolve().then(callback));
  notify(() => {
    onError?.(error);
    onClose?.({ code: 1008, reason: error.message, wasClean: true });
  });

  return {
    send() {
      return false;
    },

    close() {
      // No browser socket was opened, so there is nothing to close.
    },

    get readyState() {
      return 3;
    },

    get disabled() {
      return true;
    },
  };
}

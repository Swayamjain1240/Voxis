const WS_URL =
  import.meta.env.VITE_WS_URL ||
  "ws://127.0.0.1:8000/ws";

export function createWebSocketClient({
  onOpen,
  onMessage,
  onClose,
  onError,
} = {}) {
  const socket = new WebSocket(
    WS_URL
  );

  socket.addEventListener(
    "open",
    () => onOpen?.()
  );

  socket.addEventListener(
    "message",
    (event) => {
      let payload = event.data;

      try {
        payload = JSON.parse(
          event.data
        );
      } catch {
        // Plain text is valid.
      }

      onMessage?.(payload);
    }
  );

  socket.addEventListener(
    "close",
    (event) => onClose?.(event)
  );

  socket.addEventListener(
    "error",
    (event) => onError?.(event)
  );

  return {
    send(payload) {
      if (
        socket.readyState ===
        WebSocket.OPEN
      ) {
        socket.send(
          JSON.stringify(payload)
        );

        return true;
      }

      return false;
    },

    close() {
      socket.close();
    },

    get readyState() {
      return socket.readyState;
    },
  };
}

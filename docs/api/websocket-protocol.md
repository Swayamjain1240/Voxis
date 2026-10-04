# SilentSign — WebSocket Protocol

## 1. Purpose

WebSocket support is used for real-time communication and later for Mode 2 room-based conversations.

Mode 1 should not depend on remote WebSockets unless required by the chosen inference architecture.

> Status: **Planned protocol**.

---

## 2. Connection

Development endpoint:

```text
ws://localhost:8000/ws
```

Mode 2 room endpoint may later be:

```text
ws://localhost:8000/ws/rooms/{room_code}
```

Production must use:

```text
wss://
```

---

## 3. Event Envelope

All WebSocket messages should use one standard envelope:

```json
{
  "type": "event_name",
  "id": "evt_001",
  "timestamp": 1791107414,
  "payload": {}
}
```

Optional metadata:

```json
{
  "type": "event_name",
  "id": "evt_001",
  "timestamp": 1791107414,
  "payload": {},
  "meta": {
    "session_id": "session_001",
    "room_code": "482913",
    "protocol_version": "1"
  }
}
```

---

## 4. Core Event Types

Recommended initial event names:

```text
client_ready
server_ready

landmark_frame
sign_prediction
sign_sequence_complete

audio_chunk
speech_transcript

text_to_gloss_result
avatar_sequence

conversation_message

error
ping
pong
```

Mode 2 later:

```text
room_joined
room_left
peer_joined
peer_left
```

---

## 5. `client_ready`

Client → Server

```json
{
  "type": "client_ready",
  "id": "evt_001",
  "timestamp": 1791107414,
  "payload": {
    "client": "web",
    "context": "hospital",
    "vocabulary_version": "0.1.0"
  }
}
```

---

## 6. `server_ready`

Server → Client

```json
{
  "type": "server_ready",
  "id": "evt_002",
  "timestamp": 1791107415,
  "payload": {
    "api_version": "v1",
    "model_version": "0.1.0",
    "vocabulary_version": "0.1.0"
  }
}
```

---

## 7. `landmark_frame`

Client → Server

Use only if sign inference runs server-side.

```json
{
  "type": "landmark_frame",
  "id": "evt_003",
  "timestamp": 1791107416,
  "payload": {
    "sequence_id": "seq_001",
    "frame_index": 12,
    "left_hand": [],
    "right_hand": [],
    "pose": []
  }
}
```

For efficiency, later optimization may batch frames instead of sending every frame individually.

---

## 8. `sign_prediction`

Server → Client

```json
{
  "type": "sign_prediction",
  "id": "evt_004",
  "timestamp": 1791107417,
  "payload": {
    "gloss": "PAIN",
    "confidence": 0.91,
    "alternatives": [
      {
        "gloss": "HELP",
        "confidence": 0.04
      }
    ]
  }
}
```

Unknown:

```json
{
  "type": "sign_prediction",
  "id": "evt_005",
  "timestamp": 1791107418,
  "payload": {
    "gloss": "UNKNOWN",
    "confidence": 0.42
  }
}
```

---

## 9. `sign_sequence_complete`

Client or Server → Peer/Server

```json
{
  "type": "sign_sequence_complete",
  "id": "evt_006",
  "timestamp": 1791107419,
  "payload": {
    "glosses": ["PAIN", "YESTERDAY"],
    "context": "hospital"
  }
}
```

---

## 10. `speech_transcript`

Server → Client

```json
{
  "type": "speech_transcript",
  "id": "evt_007",
  "timestamp": 1791107420,
  "payload": {
    "text": "Where does it hurt?",
    "language": "en",
    "confidence": 0.93
  }
}
```

---

## 11. `text_to_gloss_result`

Server → Client

```json
{
  "type": "text_to_gloss_result",
  "id": "evt_008",
  "timestamp": 1791107421,
  "payload": {
    "glosses": ["WHERE", "PAIN"],
    "unsupported_words": []
  }
}
```

---

## 12. `avatar_sequence`

Server → Client

```json
{
  "type": "avatar_sequence",
  "id": "evt_009",
  "timestamp": 1791107422,
  "payload": {
    "glosses": ["WHERE", "PAIN"]
  }
}
```

The frontend is responsible for mapping gloss IDs to available animation clips.

---

## 13. `conversation_message`

Either direction:

```json
{
  "type": "conversation_message",
  "id": "evt_010",
  "timestamp": 1791107423,
  "payload": {
    "message_id": "msg_001",
    "source": "hearing-user",
    "input_type": "speech",
    "text": "Where does it hurt?",
    "glosses": ["WHERE", "PAIN"]
  }
}
```

---

## 14. Error Event

Server → Client

```json
{
  "type": "error",
  "id": "evt_011",
  "timestamp": 1791107424,
  "payload": {
    "code": "MODEL_UNAVAILABLE",
    "message": "Sign recognition is temporarily unavailable.",
    "recoverable": true
  }
}
```

Do not send:
- Python tracebacks
- API keys
- environment values
- internal filesystem paths

---

## 15. Heartbeat

Client:

```json
{
  "type": "ping",
  "id": "evt_ping_001",
  "timestamp": 1791107425,
  "payload": {}
}
```

Server:

```json
{
  "type": "pong",
  "id": "evt_pong_001",
  "timestamp": 1791107425,
  "payload": {}
}
```

This helps detect dead connections.

---

## 16. Mode 2 Room Events

Later protocol:

```text
room_joined
peer_joined
peer_left
room_closed
```

Example:

```json
{
  "type": "peer_joined",
  "id": "evt_020",
  "timestamp": 1791107500,
  "payload": {
    "peer_id": "peer_002"
  },
  "meta": {
    "room_code": "482913"
  }
}
```

Do not expose unnecessary personal identity information.

---

## 17. Validation Rules

Every incoming event must validate:

```text
type
id
timestamp
payload shape
allowed enum values
vocabulary version where applicable
room membership where applicable
```

Unknown event type:

```json
{
  "type": "error",
  "id": "evt_error_001",
  "timestamp": 1791107426,
  "payload": {
    "code": "INVALID_EVENT",
    "message": "Unsupported WebSocket event type.",
    "recoverable": true
  }
}
```

---

## 18. Rate / Size Controls

Protect the server from:

- oversized payloads
- excessive event frequency
- malformed landmark arrays
- excessive audio streaming
- room spam

Do not accept unlimited binary or JSON messages.

---

## 19. Reconnection Strategy

Frontend should use:

```text
connected
  ↓
connection lost
  ↓
short retry delay
  ↓
reconnect
  ↓
restore session if valid
```

Avoid infinite aggressive reconnect loops.

---

## 20. Protocol Versioning

Include:

```json
{
  "protocol_version": "1"
}
```

Breaking WebSocket message changes require a version update.

Canonical schema:

```text
shared/contracts/websocket-events.schema.json
```

---

## 21. Backend Structure

```text
backend/app/websocket/
├── manager.py
├── handlers.py
└── events.py
```

Responsibilities:

- `manager.py` → connections and rooms
- `handlers.py` → incoming event dispatch
- `events.py` → event definitions/helpers

---

## 22. Mode 1 vs Mode 2 Rule

### Mode 1

Prefer the simplest reliable architecture.

Do not force WebSocket complexity if local/browser processing plus normal REST calls are sufficient.

### Mode 2

WebSocket becomes important for:
- room presence
- real-time message exchange
- landmark/text transfer
- peer state

Mode 2 is a later milestone, not a blocker for the first SilentSign MVP.

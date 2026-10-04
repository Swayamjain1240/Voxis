# SilentSign — API Overview

## 1. Purpose

This document defines the planned API contract between the SilentSign frontend, backend, ML runtime, speech services, and optional Mode 2 real-time communication.

The API is designed around:

- React + Vite + TypeScript frontend
- FastAPI backend
- REST for request/response operations
- WebSocket for real-time communication
- Shared versioned contracts
- Predictable validation and error responses

> Status: **Architecture contract / planned API**.  
> Endpoints documented here are not considered implemented until the corresponding phase is completed and tested.

---

## 2. API Base

Recommended development base URL:

```text
http://localhost:8000/api/v1
```

Recommended production shape:

```text
https://<backend-domain>/api/v1
```

WebSocket base:

```text
ws://localhost:8000/ws
```

Production:

```text
wss://<backend-domain>/ws
```

---

## 3. Versioning

All REST routes use explicit API versioning:

```text
/api/v1/...
```

Breaking contract changes require a new version:

```text
/api/v2/...
```

Do not silently change existing response shapes.

---

## 4. Planned REST Route Groups

```text
/api/v1/
├── health
├── sign
├── speech
├── conversation
└── rooms          # Mode 2 later
```

Corresponding FastAPI structure:

```text
backend/app/api/v1/
├── router.py
└── routes/
    ├── health.py
    ├── sign.py
    ├── speech.py
    ├── conversation.py
    └── rooms.py
```

---

## 5. Standard Success Envelope

Recommended format:

```json
{
  "success": true,
  "data": {},
  "meta": {
    "request_id": "req_123",
    "api_version": "v1"
  }
}
```

For simple responses, `meta` may contain only fields that are useful.

---

## 6. Standard Error Envelope

All API errors should use one consistent structure:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request could not be processed.",
    "details": {}
  },
  "meta": {
    "request_id": "req_123",
    "api_version": "v1"
  }
}
```

Do not return raw Python exceptions or stack traces to clients.

---

## 7. Recommended Error Codes

```text
INVALID_REQUEST
VALIDATION_ERROR
UNSUPPORTED_MEDIA_TYPE
AUDIO_TOO_SHORT
NO_SPEECH_DETECTED
TRANSCRIPTION_FAILED
UNKNOWN_GLOSS
LOW_CONFIDENCE
MODEL_UNAVAILABLE
LLM_UNAVAILABLE
TTS_UNAVAILABLE
ROOM_NOT_FOUND
ROOM_FULL
RATE_LIMITED
INTERNAL_ERROR
```

---

## 8. Core Data Contracts

### Sign Prediction

```json
{
  "gloss": "PAIN",
  "confidence": 0.91,
  "timestamp": 1791107414,
  "model_version": "0.1.0",
  "vocabulary_version": "0.1.0"
}
```

### Unknown Prediction

```json
{
  "gloss": "UNKNOWN",
  "confidence": 0.42,
  "alternatives": [
    {
      "gloss": "PAIN",
      "confidence": 0.42
    },
    {
      "gloss": "HELP",
      "confidence": 0.31
    }
  ]
}
```

### Speech Result

```json
{
  "text": "Where does it hurt?",
  "language": "en",
  "confidence": 0.93
}
```

### Text-to-Gloss Result

```json
{
  "glosses": ["WHERE", "PAIN"],
  "unsupported_words": []
}
```

### Conversation Message

```json
{
  "id": "msg_001",
  "source": "signer",
  "input_type": "sign",
  "text": "I am in pain.",
  "glosses": ["PAIN"],
  "timestamp": 1791107414
}
```

---

## 9. Shared Contract Ownership

Canonical schemas should live in:

```text
shared/contracts/
├── sign-prediction.schema.json
├── speech-result.schema.json
├── websocket-events.schema.json
└── conversation-message.schema.json
```

Canonical vocabulary should live in:

```text
shared/vocabulary/
├── vocabulary.json
├── label_map.json
└── contexts.json
```

Frontend and backend must consume the same contract definitions.

---

## 10. Context Modes

Initial planned values:

```text
hospital
bank
office
```

Context must influence language conversion and quick phrases, but it must **not** bypass the supported vocabulary.

Example:

```json
{
  "context": "hospital",
  "glosses": ["PAIN"]
}
```

---

## 11. Security Requirements

The backend must:

1. Keep API keys and secrets server-side.
2. Load secrets from environment variables.
3. Validate required environment variables at startup.
4. Validate all REST and WebSocket payloads.
5. Use a strict CORS allowlist.
6. Apply rate limiting where appropriate.
7. Add security headers.
8. Disable production debug mode.
9. Avoid exposing stack traces.
10. Log request IDs without logging secrets or raw sensitive media unnecessarily.

---

## 12. Media Handling

### Camera

For Mode 1, raw camera video should remain in the browser where possible.

Preferred runtime data:

```text
camera
  ↓
MediaPipe
  ↓
landmarks
```

### Microphone

Audio may be sent to the backend for Whisper transcription.

The frontend should send only the audio required for the active transcription request.

---

## 13. HTTP Status Guidance

```text
200 OK
201 Created
400 Bad Request
404 Not Found
409 Conflict
413 Payload Too Large
415 Unsupported Media Type
422 Validation Error
429 Too Many Requests
500 Internal Server Error
503 Service Unavailable
```

---

## 14. Development Rules

- Do not add an endpoint without documenting its request/response contract.
- Do not change shared schemas casually.
- Prefer typed Pydantic request/response models.
- Prefer typed TypeScript frontend contracts.
- Keep Mode 2 room APIs isolated from Mode 1 core MVP.
- Add integration tests for every endpoint before calling it stable.

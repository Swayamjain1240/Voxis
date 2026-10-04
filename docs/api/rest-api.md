# SilentSign — REST API Contract

## 1. Purpose

This file defines the planned REST endpoints for SilentSign.

> Status: **Planned contract**.  
> An endpoint becomes production-valid only after implementation, tests, and contract verification.

Base:

```text
/api/v1
```

---

## 2. Health

### GET `/health`

Checks whether the backend is running.

Response:

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "service": "silentsign-api",
    "version": "0.1.0"
  }
}
```

---

## 3. Sign Recognition

### POST `/sign/predict`

Purpose:

Receive a preprocessed landmark sequence and return one sign prediction.

Recommended only when inference is backend-hosted.

Request:

```json
{
  "frames": [
    {
      "timestamp": 1791107414,
      "left_hand": [],
      "right_hand": [],
      "pose": []
    }
  ],
  "context": "hospital",
  "vocabulary_version": "0.1.0"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "gloss": "PAIN",
    "confidence": 0.91,
    "alternatives": [
      {
        "gloss": "HELP",
        "confidence": 0.04
      }
    ],
    "model_version": "0.1.0",
    "vocabulary_version": "0.1.0"
  }
}
```

Possible errors:

```text
VALIDATION_ERROR
MODEL_UNAVAILABLE
LOW_CONFIDENCE
UNKNOWN_GLOSS
```

---

### POST `/sign/gloss-to-text`

Purpose:

Convert a validated gloss sequence into a natural-language sentence.

Request:

```json
{
  "context": "hospital",
  "language": "en",
  "glosses": ["PAIN", "YESTERDAY"]
}
```

Response:

```json
{
  "success": true,
  "data": {
    "text": "I have had pain since yesterday.",
    "glosses": ["PAIN", "YESTERDAY"]
  }
}
```

Rules:

- Never add unsupported medical facts.
- Preserve the original gloss sequence.
- If the LLM fails, return a controlled error; frontend may show raw glosses.

---

### POST `/sign/tts`

Purpose:

Convert natural-language text to speech.

Request:

```json
{
  "text": "I have pain.",
  "language": "en"
}
```

Possible response strategy:

```json
{
  "success": true,
  "data": {
    "audio_url": "/media/tts/tts_001.mp3"
  }
}
```

Exact transport may later use streaming instead.

---

## 4. Speech Recognition

### POST `/speech/transcribe`

Purpose:

Convert microphone audio to text using Whisper.

Content type:

```text
multipart/form-data
```

Suggested fields:

```text
audio
language
context
```

Response:

```json
{
  "success": true,
  "data": {
    "text": "Where does it hurt?",
    "language": "en",
    "confidence": 0.93
  }
}
```

Possible errors:

```text
AUDIO_TOO_SHORT
NO_SPEECH_DETECTED
UNSUPPORTED_MEDIA_TYPE
TRANSCRIPTION_FAILED
```

---

### POST `/speech/text-to-gloss`

Purpose:

Convert transcript text into supported ISL glosses.

Request:

```json
{
  "text": "Where does it hurt?",
  "context": "hospital",
  "language": "en"
}
```

Backend internally restricts output using `shared/vocabulary`.

Response:

```json
{
  "success": true,
  "data": {
    "glosses": ["WHERE", "PAIN"],
    "unsupported_words": []
  }
}
```

The server must validate that every returned gloss exists in the active vocabulary.

---

## 5. Conversation

### POST `/conversation/message`

Purpose:

Store or normalize one conversation message in the active session.

For the MVP this may remain frontend-only if persistent backend storage is unnecessary.

Request:

```json
{
  "session_id": "session_001",
  "source": "signer",
  "input_type": "sign",
  "text": "I am in pain.",
  "glosses": ["PAIN"]
}
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "msg_001",
    "session_id": "session_001",
    "source": "signer",
    "input_type": "sign",
    "text": "I am in pain.",
    "glosses": ["PAIN"],
    "timestamp": 1791107414
  }
}
```

---

### DELETE `/conversation/{session_id}`

Purpose:

Clear the current conversation session.

Response:

```json
{
  "success": true,
  "data": {
    "session_id": "session_001",
    "cleared": true
  }
}
```

---

## 6. Mode 2 Rooms — Later

These endpoints are not part of the first Mode 1 milestone.

### POST `/rooms`

Creates a remote room.

Response:

```json
{
  "success": true,
  "data": {
    "room_code": "482913"
  }
}
```

### POST `/rooms/{room_code}/join`

Joins an existing room.

Response:

```json
{
  "success": true,
  "data": {
    "room_code": "482913",
    "joined": true
  }
}
```

### DELETE `/rooms/{room_code}`

Closes a room.

---

## 7. Request Validation

FastAPI/Pydantic schemas should reject:

- missing required fields
- invalid context
- unsupported language
- malformed landmark arrays
- invalid gloss labels
- oversized payloads
- unsupported audio formats

Example validation error:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body.",
    "details": {
      "field": "context"
    }
  }
}
```

---

## 8. Planned Route Files

```text
backend/app/api/v1/routes/
├── health.py
├── sign.py
├── speech.py
├── conversation.py
└── rooms.py
```

Recommended schemas:

```text
backend/app/schemas/
├── sign.py
├── speech.py
├── conversation.py
└── websocket.py
```

---

## 9. Testing Requirements

Every stable REST endpoint should have:

```text
happy-path test
validation test
service-failure test
invalid-input test
security/rate-limit test where relevant
```

Example:

```text
tests/integration/test_sign_routes.py
tests/integration/test_speech_routes.py
tests/integration/test_health.py
```

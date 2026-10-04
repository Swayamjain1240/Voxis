# SilentSign — Phase 6: Integration, Reliability & Final Application

## Objective

Merge both working pipelines into one polished SilentSign application.

Primary target: **Mode 1 face-to-face communication on one device.**

---

## 1. Final Mode 1 Flow

```text
Deaf/Sign User
   ↓
Signs to Camera
   ↓
Swayam Pipeline
   ↓
Text + Speech
   ↓
Hearing User

Hearing User
   ↓
Speaks
   ↓
Rishi Pipeline
   ↓
Captions + Avatar
   ↓
Deaf/Sign User
```

---

## 2. Frontend Integration

Main conversation screen should include:

```text
Signer Side
- Camera
- Landmark overlay
- Sign status
- Confidence
- Gloss chips

Hearing Side
- Avatar
- Captions
- Microphone
- Audio status

Shared
- Turn indicator
- Transcript
- Context selector
- Clear session
- Debug mode
```

---

## 3. Backend Integration

Integrate:

```text
FastAPI
├── sign runtime
├── speech/Whisper
├── language services
├── TTS
├── conversation
└── WebSocket layer
```

Use standardized API/error contracts.

---

## 4. Runtime/ML Optimization

Swayam:

- [ ] Export model to ONNX if appropriate
- [ ] Verify ONNX output parity
- [ ] Optimize latency
- [ ] Freeze model/vocabulary/preprocessing versions
- [ ] Add runtime health status

---

## 5. Reliability

Implement:

- [ ] camera permission fallback
- [ ] microphone permission fallback
- [ ] no-hands warning
- [ ] poor-framing warning
- [ ] low-confidence handling
- [ ] unknown sign handling
- [ ] noisy-audio handling
- [ ] LLM failure fallback
- [ ] TTS failure fallback
- [ ] missing-avatar-clip fallback
- [ ] loading states
- [ ] retry states
- [ ] clear/reset

---

## 6. Debug Mode

Show:

```text
camera status
landmark status
buffer length
raw gloss
confidence
top predictions
model latency
LLM latency
speech latency
active avatar gloss
```

Production debug mode should remain disabled by default.

---

## 7. Security Checklist

- [ ] secrets in environment variables
- [ ] no API key in frontend
- [ ] strict CORS allowlist
- [ ] validated REST payloads
- [ ] validated WebSocket payloads
- [ ] rate limits where appropriate
- [ ] security headers
- [ ] no stack traces to client
- [ ] dependency audit
- [ ] secret scan before release

---

## 8. Testing

### Unit
- frontend feature tests
- preprocessing tests
- model helper tests
- backend service tests

### Integration
- frontend ↔ backend
- Whisper
- LLM
- TTS
- model runtime
- avatar registry

### End-to-end
At least:

```text
sign → sentence → speech
speech → gloss → avatar
```

with multiple real test users where possible.

---

## 9. Mode 2 — Only If Time Remains

After Mode 1 is stable:

```text
Create Room
   ↓
6-digit code
   ↓
Join Room
   ↓
WebSocket
   ↓
real-time text/landmark exchange
```

Do not add login/friends unless the core product is already complete.

---

## 10. Demo Readiness

Before final submission:

- [ ] stable local demo
- [ ] backup demo recording
- [ ] known test signs
- [ ] known test phrases
- [ ] dataset/source slide
- [ ] architecture slide
- [ ] accuracy report
- [ ] latency report
- [ ] limitations clearly stated
- [ ] at least five rehearsals

---

## 11. Final Definition of Done

SilentSign is ready when a face-to-face conversation can happen on one device:

```text
Sign user signs
→ hearing user reads/hears

Hearing user speaks
→ sign user reads/sees avatar
```

with stable fallbacks, known limitations, and no dependency on unfinished optional features.

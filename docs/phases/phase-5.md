# SilentSign — Phase 5: Complete Two-Way Pipelines

## Objective

Complete both translation directions independently before final application integration.

---

## 1. Swayam — Complete Sign-to-Speech

Flow:

```text
Signer
   ↓
Camera
   ↓
MediaPipe
   ↓
Sign Recognition
   ↓
Gloss Sequence
   ↓
Gloss-to-Text LLM
   ↓
Natural Sentence
   ↓
TTS
   ↓
Captions + Audio
```

### Tasks

- [ ] Final gloss-sequence builder
- [ ] Sentence completion rule
- [ ] Gloss-to-text prompt
- [ ] Context-aware sentence generation
- [ ] Preserve raw glosses
- [ ] Add TTS
- [ ] Add captions
- [ ] LLM failure fallback
- [ ] TTS failure fallback
- [ ] End-to-end latency measurement

---

## 2. Rishi — Complete Speech-to-Sign

Flow:

```text
Hearing User
   ↓
Microphone
   ↓
Whisper
   ↓
Text
   ↓
Text-to-Gloss
   ↓
Animation Lookup
   ↓
Avatar
   ↓
Captions
```

### Tasks

- [ ] Connect microphone to Whisper
- [ ] Connect transcript to LLM
- [ ] Connect glosses to animation registry
- [ ] Play complete sequence
- [ ] Highlight captions
- [ ] Unsupported-word fallback
- [ ] Missing-animation fallback
- [ ] Full retry flow
- [ ] End-to-end latency measurement

---

## 3. Integration Contract

Both directions should generate conversation messages with one shared shape.

Example:

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

## 4. Phase 5 Deliverables

### Swayam
A complete Sign → Text/Speech demo.

### Rishi
A complete Speech → Text → Sign Avatar demo.

---

## 5. Definition of Done

Phase 5 passes when both pipelines work independently from real input to final output without manual internal intervention.

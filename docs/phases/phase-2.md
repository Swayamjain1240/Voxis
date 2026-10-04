# SilentSign — Phase 2: Data & Speech Preparation

## Objective

Prepare production-quality model input on Swayam's side and reliable speech transcription on Rishi's side.

---

## 1. Swayam — ML Data Pipeline

Flow:

```text
Dataset Videos
   ↓
Canonical MediaPipe Extraction
   ↓
Missing Landmark Handling
   ↓
Normalization
   ↓
Fixed-Length Sequences
   ↓
Signer-Aware Split
   ↓
Training-Ready Dataset
```

### Tasks

- [ ] Batch landmark extraction
- [ ] Canonical feature ordering
- [ ] Missing-hand handling
- [ ] Invalid clip rejection
- [ ] Shoulder-centered normalization
- [ ] Scale normalization
- [ ] Pad/trim sequences
- [ ] Define target sequence length
- [ ] Generate labels
- [ ] Build train/validation/test manifests
- [ ] Prevent signer leakage
- [ ] Prevent raw/cropped duplicate leakage
- [ ] Add preprocessing tests
- [ ] Save preprocessing version/config

### ML ownership

```text
ml/sign-recognition/src/extraction/
ml/sign-recognition/src/preprocessing/
ml/sign-recognition/src/datasets/
```

---

## 2. Rishi — Speech-to-Text

Flow:

```text
Microphone
   ↓
Audio File/Blob
   ↓
Backend
   ↓
Whisper
   ↓
Transcript
```

### Tasks

- [ ] Define audio format
- [ ] Send audio to backend
- [ ] FastAPI upload endpoint
- [ ] Whisper service
- [ ] English transcription first
- [ ] Handle silence
- [ ] Handle short/noisy audio
- [ ] Return structured transcript
- [ ] Show transcript in frontend
- [ ] Add retry flow

---

## 3. Backend Work

Create:

```text
backend/app/services/speech/
├── whisper_service.py
└── audio_processor.py
```

and:

```text
backend/app/api/v1/routes/speech.py
```

---

## 4. Phase 2 Deliverables

### Swayam
A training-ready dataset with reproducible preprocessing.

### Rishi
A reliable:

```text
microphone → Whisper → text
```

pipeline.

---

## 5. Definition of Done

Phase 2 passes when:

- [ ] Swayam can regenerate ML tensors from manifests.
- [ ] Train/test splits are signer-aware.
- [ ] Preprocessing is deterministic.
- [ ] Rishi can speak one sentence and receive the correct transcript.
- [ ] Errors are handled without crashing.

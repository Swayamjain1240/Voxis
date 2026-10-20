# VOXIS — Phase 2: Data & Speech Preparation

> **Status: Source implementation complete; runtime data/model verification
> pending.** Phase 2 source deliverables are implemented and tested. A real
> training dataset and local Whisper model are not included in this checkout,
> so no accuracy or spoken-sentence result is claimed.

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

### Tasks and current status

- [x] Batch landmark extraction
- [x] Canonical feature ordering
- [x] Missing-hand handling
- [x] Invalid clip rejection with a rejection manifest
- [x] Shoulder-centered normalization
- [x] Scale normalization
- [x] Pad/trim sequences
- [x] Define target sequence length
- [x] Generate labels
- [x] Build train/validation/test manifests
- [x] Prevent signer leakage
- [x] Prevent raw/cropped duplicate leakage
- [x] Add preprocessing tests
- [x] Save preprocessing version/config

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

### Tasks and current status

- [x] Define supported audio formats and bounded upload behavior
- [x] Send audio to backend
- [x] FastAPI upload and transcription endpoints
- [x] Optional local faster-whisper service adapter
- [x] English transcription contract
- [x] Handle silence and too-short WAV audio
- [x] Report unknown quality for compressed formats that need a decoder
- [x] Return structured transcript
- [x] Show transcript in frontend
- [x] Add retry flow

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
A reproducible manifest-driven dataset preparation flow with processed
sequences, rejection reports, preprocessing metadata, and signer-isolated split
manifests. A real dataset is still supplied outside Git.

### Rishi
A bounded microphone-to-transcription source flow using an optional local
Whisper runtime:

```text
microphone → Whisper → text
```

pipeline.

---

## 5. Definition of Done

The source implementation passes when:

- [x] Swayam can regenerate ML tensors from manifests.
- [x] Train/test splits are signer-aware.
- [x] Preprocessing is deterministic.
- [ ] Rishi can speak one sentence and receive the correct transcript in this
  checkout; this needs the optional faster-whisper package, a local model, and
  a real audio run.
- [x] Errors are handled without crashing.

## Build Phase 2 delivery

The five pushed checkpoints on `main` are:

1. `1fdaf24` — versioned preprocessing contract and deterministic augmentation;
2. `7cbb203` — manifest-driven preparation and per-sample seeds;
3. `9d9351f` — audio duration/quality contract and silence/short-input guards;
4. `ad4b990` — optional local Whisper adapter and transcript/retry UI;
5. final split-manifest, rejection-report, documentation, and Duck checkpoint.

Evidence for the source implementation:

- focused ML tests: **26 passed**;
- backend regression suite: **102 passed**;
- frontend tests: **26 passed**;
- frontend production build: completed with existing Vite warnings;
- ML source/scripts compile successfully;
- no real dataset, model artifact, API key, or external provider was added.

The optional speech runtime is documented in `backend/requirements-speech.txt`
and is disabled unless `WHISPER_ENABLED=true` is explicitly configured. The
current environment does not have `faster-whisper`, so real transcription is
not claimed. The injected-model backend test proves the structured response
contract without fabricating a production transcript.

## Final Duck review — Build Phase 2

**Verdict: DUCK PASS WITH GAPS.**

The Phase 2 source work is complete for its reproducible data and speech
preparation scope. The remaining evidence gap is environmental and explicit:
install the optional local Whisper runtime, provide a local model, and run a
real spoken sentence through the browser/backend flow. No Phase 3 work starts
from this checkpoint; wait for the user's explicit command.

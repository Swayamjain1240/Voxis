# VOXIS — Phase 1: Input Foundation

## Status

**Overall status: Source foundation implemented; live asset verification pending.**

This phase now has source-backed microphone/avatar behavior and a connected,
asset-gated browser sign-capture foundation. It does **not** claim a complete
translation product: no trained sign model, Whisper pipeline, or full
translation flow is active, and a live browser run with local MediaPipe assets
has not been performed in this checkout.

The status below is source-backed and is supplemented by the current checks in
`docs/part-1.md`; it does not claim that the full product flow is complete.
See [`docs/security-threat-model.md`](../security-threat-model.md) for the
security/architecture status register.

| Area | Status | Current evidence |
| --- | --- | --- |
| Speech input foundation | **Implemented (source)** | `useMicrophone`, audio recorder, permission/error states, track cleanup, and local audio Blob preview are used by the Home page. |
| Avatar foundation | **Implemented (source)** | A procedural Three.js avatar renders idle/wave/sign gestures; a GLB loading boundary exists behind an environment URL. |
| Sign input foundation | **Implemented (source)** | Conversation route mounts camera lifecycle, video, landmark overlay, canonical normalization, bounded sequence capture, status/error states, and local JSON sequence export; model prediction remains disabled. |
| Browser MediaPipe processing | **Implemented (source, asset-gated)** | `useMediaPipe` creates a configured Tasks Vision Holistic Landmarker when local model/WASM paths are supplied; blank paths remain an explicit `not_configured` state. |
| Shared vocabulary/contracts | **Implemented (source/docs)** | The versioned 12-gloss vocabulary, label map, contexts, and JSON contracts exist. |
| Backend connection | **Partial / scaffold** | Health, bounded/content-validated audio upload, typed REST contracts, security limits, and a disabled WebSocket boundary exist; Whisper and sign inference are disabled by default. |

## Objective

Build independently usable input foundations for both sides of VOXIS. No model
training or translation claim belongs in this phase.

## 1. Sign input foundation

### Target flow

```text
Browser Camera
   ↓
Live Video
   ↓
MediaPipe
   ↓
Hand + Pose Landmarks
   ↓
Landmark Overlay
   ↓
Canonical Landmark Frame
   ↓
30–60 Frame Buffer
```

### Source-backed pieces

The following reusable pieces are present:

- `frontend/src/features/sign-input/hooks/useCamera.js` — camera permission,
  stream state, and track cleanup.
- `frontend/src/features/sign-input/components/CameraFeed.jsx` — local video
  element binding.
- `frontend/src/features/sign-input/components/LandmarkOverlay.jsx` — point
  overlay surface.
- `frontend/src/features/sign-input/services/landmarkExtractor.js` — basic
  normalization and flattening helpers.
- `frontend/src/features/sign-input/services/frameBuffer.js` — bounded frame
  buffer utility.

### Remaining verification and later work

- A live browser run still needs local Tasks Vision model/WASM assets and
  camera permission/E2E verification.
- No live sign prediction, confidence, or model inference is part of Phase 1.
- Sequence JSON export is a local debugging handoff, not a backend upload or
  accuracy result.

### Sign-side status

**Implemented in source; asset-gated at runtime.** The target flow is wired in
the Conversation route, but a browser demonstration requires local public
MediaPipe assets and a separate manual/E2E verification pass.

## 2. Speech and avatar foundation

### Target flow

```text
Microphone
   ↓
Audio Capture

and

3D Avatar
   ↓
Browser Render
   ↓
Basic Idle / Test Animation
```

### Source-backed behavior

- `useMicrophone` requests permission, records with `MediaRecorder`, reports
  status/errors, tracks duration, releases tracks, and exposes the captured
  Blob for local playback.
- The Home page renders the microphone controls and audio preview.
- `SignAvatar` renders a procedural avatar with idle, wave, and sign gesture
  controls through React Three Fiber/Three.js.
- A configured GLB can be loaded through `VITE_AVATAR_MODEL_URL`, but no final
  ISL sign-animation library is included.

### Speech/avatar status

**Implemented (source) for the local foundation slice; not a speech-to-sign
pipeline.** Whisper transcription, text-to-gloss conversion from real speech,
animation lookup, and signed response playback are later-phase work.

## 3. Shared contract

Both pipelines use the same versioned labels and contracts:

```text
shared/vocabulary/vocabulary.json
shared/vocabulary/label_map.json
shared/vocabulary/contexts.json
shared/contracts/
```

The current contract contains 12 uppercase glosses:

```text
DOCTOR PATIENT MEDICINE SICK YESTERDAY BANK
MONEY YES NO WHERE HELP PAIN
```

This fixed vocabulary is a Phase 1 foundation constraint. It is not the final
30–50 sign target and does not support unrestricted continuous ISL translation.

## 4. Phase 1 deliverables and status

| Deliverable | Status |
| --- | --- |
| Microphone permission and local capture | **Implemented (source)** |
| Audio status and cleanup | **Implemented (source)** |
| Local audio Blob preview | **Implemented (source)** |
| Procedural avatar render | **Implemented (source)** |
| Basic avatar test gestures | **Implemented (source)** |
| Camera permission and stream lifecycle utility | **Implemented (source)** |
| Browser MediaPipe setup | **Implemented (source, asset-gated)** |
| Left/right hand and pose extraction in the browser | **Implemented (source, asset-gated)** |
| Visible live landmark overlay in an active route | **Implemented (source, asset-gated)** |
| Canonical live landmark frame | **Implemented (source)** |
| Sliding 30–60 frame buffer in the active flow | **Implemented (source, 60-frame target)** |
| Saved/debugged live landmark sequence | **Implemented (local JSON export)** |
| Camera/microphone failure UX across the complete flow | **Implemented (source foundation)** |
| Trained sign model, Whisper, LLM, TTS, and final sign clips | **Deferred to later phases** |

## 5. Definition of done

The source foundation is complete when both independent flows are wired and
testable:

```text
Sign side:
camera → live MediaPipe landmarks → canonical buffered sequence

Speech/avatar side:
microphone capture works → avatar loads/renders and moves
```

The speech/avatar line and the sign-side capture line are now represented in
source. The overall product phase remains **runtime-verification pending** until
local assets and a browser demonstration are available.

## 6. Explicitly out of scope for Phase 1

- Transformer/Conformer training or accuracy claims.
- Whisper transcription (audio capture/upload is not transcription).
- LLM-backed gloss/text conversion.
- Text-to-speech.
- Final avatar sign library or real ISL animation coverage.
- End-to-end conversation integration.
- Mode 2 rooms, QR joining, or remote communication.
- Authentication, accounts, database, administrator controls, backups, and
  production deployment controls.

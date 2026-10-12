# VOXIS — Phase 1: Input Foundation

## Status

**Overall status: In progress / partial.**

This phase has a source-backed microphone/avatar foundation and a partial
camera/sign-input scaffold. It does **not** yet meet the full Phase 1
definition of done because the browser camera → MediaPipe → buffered landmark
path is not connected end to end.

The status below is source-backed and is supplemented by the current checks in
`docs/part-1.md`; it does not claim that the full product flow is complete.
See [`docs/security-threat-model.md`](../security-threat-model.md) for the
security/architecture status register.

| Area | Status | Current evidence |
| --- | --- | --- |
| Speech input foundation | **Implemented (source)** | `useMicrophone`, audio recorder, permission/error states, track cleanup, and local audio Blob preview are used by the Home page. |
| Avatar foundation | **Implemented (source)** | A procedural Three.js avatar renders idle/wave/sign gestures; a GLB loading boundary exists behind an environment URL. |
| Sign input foundation | **Partial / scaffold** | Camera lifecycle, video component, landmark overlay, normalization helpers, and `FrameBuffer` exist. |
| Browser MediaPipe processing | **Partial / scaffold** | `useMediaPipe` is an adapter boundary; its initializer does not create a MediaPipe processor and no current route mounts the sign-input flow. |
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

### Not complete yet

- The browser MediaPipe dependency/processor is not wired into
  `useMediaPipe.js`; `initialize()` currently only changes adapter state.
- The sign-input components are not mounted in the current application routes.
- The camera result is not connected to a canonical frame buffer in a user flow.
- No live sign prediction, confidence, or model inference is part of Phase 1.

### Sign-side status

**Partial / scaffold only.** Do not describe the current repository as having a
working live landmark pipeline until the target flow above is implemented and
separately verified.

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
| Camera permission and stream lifecycle utility | **Partial / scaffold** |
| Browser MediaPipe setup | **Partial / scaffold** |
| Left/right hand and pose extraction in the browser | **Planned** |
| Visible live landmark overlay in an active route | **Planned** |
| Canonical live landmark frame | **Partial / scaffold** |
| Sliding 30–60 frame buffer in the active flow | **Partial / scaffold** |
| Saved/debugged live landmark sequence | **Planned** |
| Camera/microphone failure UX across the complete flow | **Partial / scaffold** |
| Trained sign model, Whisper, LLM, TTS, and final sign clips | **Deferred to later phases** |

## 5. Definition of done

Phase 1 is complete only when both independent flows are demonstrated and
verified:

```text
Sign side:
camera → live MediaPipe landmarks → canonical buffered sequence

Speech/avatar side:
microphone capture works → avatar loads/renders and moves
```

The speech/avatar line is represented in source. The sign-side line remains
open, so the overall phase remains **in progress / partial**.

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

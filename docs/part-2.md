# Fixing Part 2 — Browser and conversation foundation

## Scope

Fixing Part 2 connects the existing camera, microphone, frame-buffer, REST, and
conversation UI foundations. It does not train a model, add Whisper, add an LLM
provider, add TTS, or enable Mode 2 WebSockets.

The target is an honest local foundation flow:

```text
context → permission/readiness → camera landmarks or microphone Blob
        → bounded local/API boundary → visible state/error → clear session
```

## Environment boundary

Backend and frontend use separate ignored `.env` files and committed examples.
No API key is required for this part. Optional MediaPipe model and WASM paths
are public asset settings documented in `docs/environment.md`; if they are
blank, the camera preview remains usable and reports `not_configured` instead
of pretending that landmark inference is active.

## Acceptance criteria

- A real camera route requests permission, displays local video, and cleans up
  tracks on stop/unmount.
- The MediaPipe adapter has an explicit configured/unconfigured/error state.
- Canonical frames are 75 landmarks × 4 values = 300 finite features.
- A bounded buffer retains at most 60 frames and exposes a full sequence only
  when 60 valid frames exist.
- A real microphone Blob can be uploaded through the existing bounded REST
  boundary; no transcript is fabricated while Whisper is disabled.
- Conversation context, turn state, transcript, glosses, and clear/reset are
  visible in the Mode 1 screen.
- Permission, unavailable-device, no-input, timeout, and disabled-service
  states are user-visible and safe.
- Backend/frontend `.env` files remain untracked; examples contain no secrets.

## Implementation checkpoints

Part 2 is being delivered as coherent pushed checkpoints on `Swayam`:

1. `81d27f3` — separate environment boundary and public asset configuration;
2. `705f30c` — canonical 75-landmark/300-feature frame contract and buffer;
3. `f735675` — Tasks Vision Holistic Landmarker adapter and dependency;
4. `ab3ffb6` — camera lifecycle, video ref, and capture loop;
5. `1b6bf92` — context/conversation foundation screen;
6. `c3a8993` — honest microphone upload validation flow.

No API key or provider was introduced. The optional MediaPipe model and WASM
paths are public/local assets; with blank paths, the app intentionally shows a
camera preview and `not_configured` rather than claiming landmark inference.

Fixing Part 2 is complete only after its implementation tests, frontend tests,
build, documentation, and Duck review pass. Part 3 must wait for an explicit
user command.

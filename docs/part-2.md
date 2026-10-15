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
6. `c3a8993` — honest microphone upload validation flow;
7. `ef2b4f5` — recorder/conversation tests and status synchronization.

No API key or provider was introduced. The optional MediaPipe model and WASM
paths are public/local assets; with blank paths, the app intentionally shows a
camera preview and `not_configured` rather than claiming landmark inference.

Fixing Part 2 is complete only after its implementation tests, frontend tests,
build, documentation, and Duck review pass. Part 3 must wait for an explicit
user command.

## Final Duck review — Fixing Part 2

**Verdict: DUCK PASS WITH GAPS.**

The Part 2 foundation now has a real route-level browser capture flow: the
Conversation screen selects hospital/bank/office context, requests camera
permission, displays local video, maps configured MediaPipe Holistic results to
the canonical 75-landmark order, buffers at most 60 valid 300-feature frames,
and cleans up camera/processor resources. The microphone flow records locally,
allows an explicit bounded upload validation request, preserves the actual MIME
type, and reports upload failures without fabricating a transcript. Local
conversation state exposes turn, transcript, glosses, and clear/reset.

Environment boundaries are separated and documented:

```text
backend/.env.example  → backend/.env
frontend/.env.example → frontend/.env
```

No API key, provider, credential, or real `.env` file was added. MediaPipe
model/WASM values are public/local asset paths; blank values produce the honest
`not_configured` state. The frontend WebSocket client remains disabled in Mode 1.

Evidence for this review:

- backend pytest: **98 passed**;
- frontend Vitest: **18 passed**;
- frontend Vite build: completed with the existing React Router directive and
  large-chunk warnings;
- `pip check`: clean;
- `pip-audit`: no known vulnerabilities;
- high-severity npm audit: 0 vulnerabilities;
- `git diff --check`: clean;
- actual `.env`, tracked bytecode, key/certificate file checks: clean;
- reachable-history common-pattern secret scan: no matches.

The remaining gaps are deliberately outside this fixing part's local contract:
the repository does not include a MediaPipe model/WASM asset, so a browser run
with blank environment values cannot produce live landmarks; browser
permission/E2E and desktop/tablet/mobile accessibility verification were not
run; no trained sign model, confidence/rejection policy, Whisper, LLM, TTS,
real avatar clips, or end-to-end translation exists. Existing build/test
warnings remain recorded. These gaps must be addressed in later work, but no
Part 3 work starts from this checkpoint.

**Part 2 is complete for its defined foundation scope. Stop here and wait for
the user's explicit command before starting Fixing Part 3.**

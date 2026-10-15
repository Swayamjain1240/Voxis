# Build Phase 1 — Input foundation

## Scope

Build Phase 1 delivers the independently usable local input foundations:

```text
camera → configured MediaPipe → visible landmarks → canonical 60-frame sequence
microphone → local audio capture
avatar → local procedural render and test gestures
```

This phase does not add trained sign inference, Whisper, LLM conversion, TTS,
real sign clips, backend persistence, or Mode 2 communication.

## Five pushed checkpoints

1. `3c13c20` — capture readiness, video-dimension gating, idempotent MediaPipe
   initialization, processor cleanup, and processing errors;
2. `7396d2d` — canonical sequence validation and bounded progress helpers;
3. `e27ea90` — local, versioned JSON export for complete landmark sequences;
4. `591d37c` — accessible capture states, camera labeling, loading guards, and
   correct handling of invisible padded landmarks;
5. final documentation and Phase 1 status checkpoint.

Every checkpoint is pushed directly to `main`.

## Observable result

On the Conversation route, a user can start the camera, receive an honest
permission/unavailable state, initialize MediaPipe when local public assets are
configured, see visible landmarks, fill a bounded canonical sequence, clear
it, and download a complete sequence for local debugging. The UI does not claim
sign recognition or fabricate a gloss.

When model/WASM paths are blank, the camera preview and explicit
`not_configured` MediaPipe state remain the expected behavior. The repository
does not include a MediaPipe model asset, so a live browser run with those
values has not been claimed.

## Evidence

- Frontend Vitest: **25 passed**.
- Frontend Vite build: completed with existing module-directive and large-chunk
  warnings.
- Backend regression baseline: **98 passed**.
- `git diff --check`: clean at each pushed checkpoint.

## Remaining runtime evidence

The source flow is implemented, but manual browser/E2E verification still needs
camera permission and local Tasks Vision model/WASM assets. The next product
work may add those public assets or proceed to the next explicitly requested
phase; no trained model or external provider is implied by this build.

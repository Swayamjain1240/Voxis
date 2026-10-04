# ADR-002 — Two Vertical Developer Pipelines

**Status:** Accepted  
**Decision Scope:** Team architecture and ownership

## Context

SilentSign is being developed mainly by two developers.

The project has two primary translation directions:

```text
Sign → Text/Speech
Speech → Text → Sign Avatar
```

If both developers work layer-by-layer on the same files, one person may become blocked by the other.

## Decision

Split ownership vertically.

### Swayam

Owns the Sign → Speech pipeline:

```text
Camera
→ MediaPipe
→ preprocessing
→ sign recognition
→ gloss sequence
→ gloss-to-text
→ TTS
```

### Rishi

Owns the Speech → Sign pipeline:

```text
Microphone
→ Whisper
→ transcript
→ text-to-gloss
→ avatar lookup
→ avatar animation
```

### Shared

Both own:
- vocabulary contract
- conversation contract
- final integration
- shared UI
- shared API/WebSocket contracts

## Why

This allows both developers to build independently and minimizes deadlock.

## Consequences

Positive:
- parallel progress
- clear responsibility
- easier debugging
- smaller merge-conflict surface

Risk:
- integration can fail if shared contracts drift

Mitigation:
- use `shared/` as the canonical contract layer

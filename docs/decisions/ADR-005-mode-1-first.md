# ADR-005 — Mode 1 Face-to-Face Before Remote Mode

**Status:** Accepted  
**Decision Scope:** Product roadmap

## Context

SilentSign can support:
- Mode 1: face-to-face on one device
- Mode 2: remote communication with room code
- future login/friends

Mode 1 demonstrates the core AI value with substantially less infrastructure.

## Decision

Build in this order:

```text
1. Mode 1 — face-to-face
2. Mode 2a — room code, only if time permits
3. Login/friends — future scope
```

## Mode 1 Must Include

- camera
- sign recognition
- captions
- TTS
- microphone
- Whisper
- text-to-gloss
- avatar
- transcript
- clear/reset
- debug visibility

## Consequences

Positive:
- reduces scope risk
- maximizes demo reliability
- keeps focus on AI

Trade-off:
- remote communication may not ship in first version

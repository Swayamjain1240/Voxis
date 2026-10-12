# ADR-008 — REST for Request/Response, WebSocket for Real-Time and Mode 2

**Status:** Accepted for future Mode 2; disabled in current Mode 1
**Decision Scope:** Backend communication

## Context

VOXIS needs both normal request/response operations and potentially real-time remote communication.

Not every operation needs a WebSocket.

## Decision

Use:

### REST

For:
- health checks
- audio transcription requests
- gloss-to-text
- text-to-gloss
- TTS requests
- simple conversation operations

### WebSocket (future Mode 2 only)

For:
- Mode 2 room presence
- real-time peer messages
- optional real-time landmark streaming
- connection state
- low-latency event exchange

## Mode 1 Rule

Do not force WebSocket complexity into Mode 1 if:
- browser-local inference
- REST calls

are sufficient.

## API Versioning

REST:

```text
/api/v1/
```

WebSocket events:

```text
protocol_version: "1"
```

## Consequences

Positive:
- simpler Mode 1
- real-time capability remains available
- clear communication semantics

Trade-off:
- two transport styles to maintain

## Current foundation rule

The current checkout does not accept WebSocket handshakes, emit events, or
broadcast messages. The old global broadcast implementation was removed after
the REST contract checkpoint. Mode 1 uses REST and browser-local capture. A
future Mode 2 implementation must add authentication, room/resource
authorization, event validation, per-connection limits, and isolation before
changing this boundary.

# ADR-008 — REST for Request/Response, WebSocket for Real-Time and Mode 2

**Status:** Accepted  
**Decision Scope:** Backend communication

## Context

SilentSign needs both normal request/response operations and potentially real-time remote communication.

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

### WebSocket

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

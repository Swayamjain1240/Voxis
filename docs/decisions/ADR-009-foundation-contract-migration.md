# ADR-009 — Freeze foundation message contracts

Status: Accepted for Fixing Part 1. Refines ADR-008's transport boundary.

The original API docs, JSON schemas, and runtime had incompatible draft shapes.
Use `shared/contracts/` as the serialized v1 specification, Pydantic validation
at server boundaries, and contract tests checking real serialized models.

- Canonical conversation IDs are `message_id`; `id` remains an input-only alias.
- Canonical timestamps are UTC ISO-8601 strings; old millisecond numeric inputs
  are normalized at the conversation boundary. Naive timestamps are rejected.
- Messages carry schema/vocabulary version `1.0.0`. Unknown versions fail.
- Sources, context, gloss membership, dimensions, text and array sizes are bounded.
- Client-supplied conversation senders cannot impersonate system/pipeline senders.
- Sign requests contain 60 raw frames of 300 finite features in extractor order.
  This does not implement normalization or model inference.
- REST success/error envelopes are migrated with their callers. Mode 1 does not
  expose WebSocket events: the old broadcast wire format and its adapters were
  removed rather than silently mixed with the v1 REST contract. The shared
  WebSocket file is a disabled transport-status contract until a separately
  reviewed Mode 2 protocol exists.

Alternatives: preserving every incompatible draft indefinitely would create
multiple sources of truth; deleting compatibility immediately would break known
local callers. The limited input aliases above provide a clear migration path.
There is no deployed client compatibility claim. No model/provider is introduced.

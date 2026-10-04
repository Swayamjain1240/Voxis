# SilentSign — Architecture Decision Records

This folder contains Architecture Decision Records (ADRs) for important technical and product decisions in SilentSign.

Each ADR records:

- the problem/context
- the decision
- why the decision was made
- alternatives considered
- consequences
- status

## ADR Index

| ADR | Decision | Status |
|---|---|---|
| ADR-001 | Monorepo with separate frontend, backend, ML, and shared layers | Accepted |
| ADR-002 | Two vertical developer pipelines | Accepted |
| ADR-003 | Fixed-vocabulary ISL recognizer for MVP | Accepted |
| ADR-004 | Canonical MediaPipe landmark representation | Accepted |
| ADR-005 | Mode 1 face-to-face before remote mode | Accepted |
| ADR-006 | `main`, `swayam`, and `rishi` Git branch strategy | Accepted |
| ADR-007 | Curated dataset handoff at Phase 4 | Accepted |
| ADR-008 | REST for request/response, WebSocket for real-time/Mode 2 | Accepted |

## Status Values

```text
Proposed
Accepted
Superseded
Deprecated
Rejected
```

Do not silently change an accepted architecture decision.

If a major decision changes, create a new ADR and mark the old ADR as superseded.

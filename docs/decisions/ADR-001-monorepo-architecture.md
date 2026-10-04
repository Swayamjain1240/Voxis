# ADR-001 — Monorepo with Separate Frontend, Backend, ML, and Shared Layers

**Status:** Accepted  
**Project:** SilentSign  
**Decision Scope:** Repository architecture

## Context

SilentSign contains several fundamentally different workloads:

- React/Vite/TypeScript frontend
- FastAPI backend
- Python ML training and evaluation
- shared vocabulary/contracts
- dataset metadata and documentation

Mixing all code into a single backend or frontend directory would make ownership, testing, dependency management, and integration difficult.

## Decision

Use one Git repository with clear top-level boundaries:

```text
SilentSign/
├── frontend/
├── backend/
├── ml/
├── shared/
├── data/
├── docs/
├── scripts/
└── tests/
```

### Responsibilities

`frontend/`
- UI
- camera
- browser MediaPipe
- microphone
- avatar
- transcript
- debug UI

`backend/`
- FastAPI
- Whisper
- LLM services
- TTS
- model runtime orchestration
- WebSocket
- optional rooms

`ml/`
- extraction
- preprocessing
- training
- evaluation
- ONNX export

`shared/`
- vocabulary
- label map
- context definitions
- API/WebSocket schemas

## Alternatives Considered

### Separate repositories

Rejected for the hackathon because:
- shared contracts become harder to synchronize
- final integration becomes more difficult
- duplicate configuration is likely

### Put ML inside backend

Rejected because:
- offline training and online serving have different dependency/lifecycle requirements
- model experimentation would pollute backend architecture

## Consequences

Positive:
- clean ownership
- easier integration
- easier testing
- shared contracts remain centralized

Trade-off:
- requires discipline to keep boundaries intact

## Rule

Do not move training code into `backend/` or frontend-specific code into `backend/`.

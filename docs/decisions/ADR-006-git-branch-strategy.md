# ADR-006 — Git Branch Strategy: main, swayam, rishi

**Status:** Accepted  
**Decision Scope:** Source-control workflow

## Context

Two developers work in parallel and need a simple hackathon-friendly workflow.

## Decision

Use:

```text
main
├── swayam
└── rishi
```

### `main`

Stable integrated branch.

Rules:
- no normal feature development directly on `main`
- merge tested work only

### `swayam`

Swayam's active development branch.

### `rishi`

Rishi's active development branch.

## Workflow

```text
developer branch
   ↓
commit
   ↓
push
   ↓
test
   ↓
merge / pull request
   ↓
main
```

After another developer's work reaches `main`, update the personal branch from `main`.

## Why Not Many Short-Lived Feature Branches?

A larger Git-flow model is valid, but for a two-person hackathon team the simplified branch strategy reduces overhead.

## Consequences

Positive:
- simple mental model
- low administrative overhead
- clear ownership

Risk:
- long-lived branches can drift

Mitigation:
- sync from `main` frequently
- commit coherent changes
- avoid editing each other's owned modules without coordination

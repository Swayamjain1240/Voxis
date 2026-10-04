# ADR-004 — Canonical MediaPipe Landmark Representation

**Status:** Accepted  
**Decision Scope:** ML data representation

## Context

SilentSign uses multiple ISL datasets.

Different datasets may provide:
- raw videos
- precomputed landmarks
- different feature orders
- different missing-value conventions
- different coordinate formats

Directly combining incompatible features can corrupt training.

## Decision

All recognition-training data should pass through a **SilentSign canonical MediaPipe extraction pipeline** whenever raw video is available.

Canonical sources:

```text
INCLUDE
ISL500
40-word secondary
Rishi/VOXIS
custom recordings
        ↓
SilentSign MediaPipe extractor
        ↓
canonical landmark format
```

## Canonical Frame

Conceptually:

```text
timestamp
left_hand[]
right_hand[]
pose[]
```

The exact feature order must remain identical across:
- extraction
- preprocessing
- training
- evaluation
- live inference

## Rules

- Missing landmarks must use one consistent representation.
- Normalization must be identical in training and runtime.
- Feature-order changes require a new preprocessing version.
- Do not silently mix third-party precomputed features.

## Consequences

Positive:
- reduces dataset mismatch
- reproducible model input
- easier runtime parity

Trade-off:
- requires reprocessing videos

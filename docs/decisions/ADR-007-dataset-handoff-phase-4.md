# ADR-007 — Curated Dataset Handoff at Phase 4

**Status:** Accepted  
**Decision Scope:** Dataset sharing between developers

## Context

Swayam owns the sign-recognition training pipeline.

Rishi owns the avatar pipeline.

Rishi does not need Swayam's entire multi-gigabyte training dataset during the first phases.

Rishi already has useful local data for signs such as:

```text
PAIN
DOCTOR
HELP
```

## Decision

Dataset handoff happens at:

```text
End of Phase 3
        ↓
Shared vocabulary freeze
        ↓
Start of Phase 4
```

At that point:

1. Compare Rishi's available avatar signs with the shared vocabulary.
2. Identify missing avatar signs.
3. Swayam shares only selected approved references/landmarks needed for those signs.

## Preferred Shared Package

```text
avatar_reference/
├── YES/
├── NO/
├── WHERE/
├── MEDICINE/
└── YESTERDAY/
```

Each sign may contain:
- approved reference video if redistribution permits
- canonical landmarks
- gloss ID
- provenance
- license note

## Rules

- Do not transfer whole datasets unnecessarily.
- Do not upload multi-GB datasets to Git.
- Do not redistribute data unless its terms allow it.
- Prefer processed motion/landmark assets where appropriate and permitted.

## Consequences

Positive:
- saves storage
- reduces legal/provenance risk
- avoids duplicated data
- lets Rishi work independently through Phase 3

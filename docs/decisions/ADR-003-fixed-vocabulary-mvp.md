# ADR-003 — Fixed-Vocabulary ISL Recognizer for MVP

**Status:** Accepted  
**Decision Scope:** AI product scope

## Context

Full unrestricted continuous sign-language translation is substantially harder than isolated/focused sign recognition.

SilentSign is a hackathon project and must prioritize reliability and a working demonstration.

## Decision

The initial sign-recognition model will be a **fixed-vocabulary isolated-sign / short-phrase recognizer**.

Bootstrap vocabulary:

```text
DOCTOR
PATIENT
MEDICINE
SICK
YESTERDAY
BANK
MONEY
YES
NO
WHERE
HELP
PAIN
```

The vocabulary may expand toward approximately 30–50 focused signs after the bootstrap system works.

## Rules

- Never claim unrestricted ISL translation.
- Unknown/unsupported input must be rejected or surfaced as uncertain.
- LLM output must not invent unsupported glosses.
- Avatar playback must only use available sign clips.

## Alternatives Considered

### Continuous unrestricted translation

Rejected for MVP because:
- data requirements are much larger
- segmentation is harder
- accuracy would be less reliable
- project risk is substantially higher

## Consequences

Positive:
- realistic model scope
- measurable accuracy
- safer demo
- easier avatar mapping

Trade-off:
- limited vocabulary

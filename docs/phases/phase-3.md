# SilentSign — Phase 3: AI Core

## Objective

Build the intelligence layer for both directions.

This is the phase where Swayam trains the sign recognizer and Rishi builds text-to-gloss conversion.

---

## 1. Swayam — Sign Recognition Model

Flow:

```text
Landmark Sequence
   ↓
Transformer / Conformer
   ↓
Class Probabilities
   ↓
Predicted Gloss
```

### Tasks

- [ ] Implement baseline Transformer
- [ ] Optionally compare Conformer
- [ ] Configure feature dimension
- [ ] Configure sequence length
- [ ] Training loop
- [ ] Validation loop
- [ ] Class weighting if required
- [ ] Data augmentation
- [ ] Checkpoint saving
- [ ] Metrics
- [ ] Confusion matrix
- [ ] Held-out signer evaluation
- [ ] Confidence calibration
- [ ] Baseline UNKNOWN/rejection logic
- [ ] Save model metadata

### Required outputs

```text
best checkpoint
metrics report
confusion matrix
model version
preprocessing version
vocabulary version
```

---

## 2. Rishi — Text to ISL Gloss

Flow:

```text
Transcript
   ↓
LLM
   ↓
Restricted Gloss Sequence
```

### Tasks

- [ ] Build text-to-gloss service
- [ ] Pass active context
- [ ] Pass allowed vocabulary
- [ ] Prevent unsupported gloss generation
- [ ] Validate LLM output
- [ ] Return unsupported words separately
- [ ] Add fallback behavior
- [ ] Add prompt tests

Example:

```text
Input:
Where does it hurt?

Output:
WHERE PAIN
```

---

## 3. Shared Vocabulary Freeze

At the end of Phase 3:

```text
vocabulary.json
label_map.json
contexts.json
```

must be reviewed by both developers.

This is the major integration checkpoint.

---

## 4. Dataset Sharing Checkpoint

**End of Phase 3 / start of Phase 4**

Rishi does not need Swayam's entire dataset.

Process:

```text
Compare shared vocabulary
   ↓
Identify avatar signs Rishi already has
   ↓
Identify missing avatar signs
   ↓
Swayam shares only selected approved references/landmarks
```

---

## 5. Phase 3 Deliverables

### Swayam
A trained classifier that predicts bootstrap vocabulary signs.

### Rishi
A restricted text-to-gloss converter.

### Both
A frozen shared vocabulary contract.

---

## 6. Definition of Done

Phase 3 passes when:

- [ ] Sign model beats baseline and is tested on held-out signer(s).
- [ ] Model produces confidence scores.
- [ ] Rishi's LLM produces only supported glosses.
- [ ] Shared vocabulary is frozen for Phase 4.
- [ ] Missing avatar data is identified.

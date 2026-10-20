# VOXIS — Phase 3: AI Core

> **Status: Partial / scaffold.** Versioned model/evaluation contracts,
> calibration and rejection logic, signer-aware report generation, optional
> runtime/sidecar validation, and a restricted vocabulary-constrained gloss
> converter exist. There is no trained checkpoint, measured held-out-signer
> result, or external LLM pipeline in the current checkout.

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

- [x] Implement baseline Transformer source
- [x] Optionally compare Conformer source
- [x] Configure feature dimension and sequence length
- [x] Training and validation loop source
- [x] Class weighting helper
- [x] Data augmentation helper
- [x] Checkpoint saving and metadata contract
- [x] Metrics and calibration helpers
- [x] Confusion matrix and structured evaluation report
- [x] Held-out signer report contract
- [x] Baseline UNKNOWN/rejection logic
- [ ] Train and measure a real checkpoint on approved data

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

- [x] Build restricted text-to-gloss service boundary
- [x] Pass active context
- [x] Pass allowed vocabulary
- [x] Prevent unsupported gloss generation
- [x] Validate converter output
- [x] Return unsupported tokens separately
- [x] Add deterministic fallback behavior
- [x] Add converter contract tests

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
A versioned classifier/training contract and optional runtime boundary. A
trained classifier that predicts bootstrap vocabulary signs remains pending real
data and an approved training run.

### Rishi
A restricted text-to-gloss converter with context validation, unsupported-token
reporting, and deterministic fallback behavior. No external provider is wired.

### Both
A frozen shared vocabulary contract.

---

## 6. Definition of Done

Phase 3 passes when:

- [ ] Sign model beats baseline and is tested on held-out signer(s).
- [x] Runtime contract produces confidence scores and explicit rejection.
- [x] Converter boundary returns only supported glosses and reports unsupported tokens.
- [ ] Shared vocabulary is frozen for Phase 4.
- [ ] Missing avatar data is identified.

## Current evidence and limits

- Backend regression suite: 108 tests passing.
- Focused ML contract suite: 44 tests passing; source compilation passes.
- PyTorch is not installed in the current environment, so the real training and
  model-architecture tests are dependency-gated.
- ONNX Runtime is optional and no checkpoint/ONNX artifact is committed.
- The evaluation report is a pure report contract; it does not create accuracy
  evidence without real predictions, targets, probabilities, and signer IDs.

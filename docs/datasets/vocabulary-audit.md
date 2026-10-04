# SilentSign — Vocabulary Audit

## 1. Purpose

This document tracks the SilentSign sign vocabulary, dataset coverage, confidence in each source, and which signs are ready for the first model.

The first model is a **fixed-vocabulary isolated-sign recognizer**. It is not unrestricted continuous ISL translation.

---

## 2. Bootstrap Vocabulary — Current Lock

The current 12-sign bootstrap vocabulary is:

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

This set is sufficient to begin the early model/application phases.

It is **not** the final 30–50 sign target vocabulary.

---

## 3. Coverage Matrix

Legend:

```text
✅ strong/usable candidate
⚠ weak / needs more validation
❌ not found
— not currently needed from this source
```

| Sign | INCLUDE | ISL500 | 40-word secondary | VOXIS/Rishi | Current status |
|---|---:|---:|---:|---:|---|
| DOCTOR | ✅ 14 | — | — | ✅ 52 | READY |
| PATIENT | ✅ 14 | — | — | ❌ | READY |
| MEDICINE | ✅ 14 | — | — | ❌ | READY |
| SICK | ✅ 21 | — | — | ❌ | READY |
| YESTERDAY | ✅ 14 | — | — | ❌ | READY |
| BANK | ✅ 40 valid | — | — | ❌ | READY |
| MONEY | ✅ 14 | — | — | ❌ | READY |
| YES | ❌ in INCLUDE target search | — | ✅ 17 | ❌ | READY |
| NO | ❌ in INCLUDE target search | — | ✅ 17 | ❌ | READY |
| WHERE | ❌ in INCLUDE target search | — | ✅ 17 | ❌ | READY |
| HELP | — | — | ✅ 16 | ✅ 52 | READY |
| PAIN | ❌ in INCLUDE | ✅ strong | ❌ in 40-word target search | ✅ 52 | READY |

---

## 4. Additional Useful Signs Found

### INCLUDE

Observed during discovery:

```text
HOSPITAL
OFFICE
```

These may be promoted during vocabulary expansion.

### VOXIS / Rishi dataset

Additional emergency signs:

```text
ACCIDENT
CALL
HOT
LOSE
THIEF
```

These are not currently part of the bootstrap vocabulary.

---

## 5. Missing / Weak Target Signs

Current unresolved or weak target vocabulary:

| Sign | Status | Notes |
|---|---|---|
| FEVER | ❌ | Not found in the checked sources |
| ACCOUNT | ❌ | Not found in the checked sources |
| FORM | ❌ | Not found in the checked sources |
| SIGNATURE | ❌ | Not found in the checked sources |
| WHEN | ⚠ | Only 2 samples found in 40-word secondary |

These signs must **not block Phase 1**.

Possible later resolution:

```text
more dataset search
      ↓
verified external source
      ↓
or
      ↓
custom recordings from verified ISL references
```

---

## 6. Dataset Quality Notes

### INCLUDE

A full metadata audit found 49 label/path mismatches in 5,250 rows.

Therefore:

```text
metadata label alone → NOT trusted
clean manifest → trusted source list
```

For the current selected classes:

```text
doctor     14 valid
patient    14 valid
medicine   14 valid
sick       21 valid
yesterday  14 valid
bank       40 valid
money      14 valid
```

### ISL500 PAIN

Validated across multiple users.

Examples processed locally:

```text
User001:
175 frames
56 left-hand frames
0 right-hand frames
175 pose frames

User002:
78 frames
46 left-hand frames
2 right-hand frames
78 pose frames
```

The similar detection pattern across two people suggests the first sample was not simply corrupt.

### 40-word YES

Validated through the same extraction pipeline:

```text
163 frames
49 left-hand frames
0 right-hand frames
163 pose frames
```

### VOXIS PAIN

```text
52 videos
26 participants
0 video read errors
```

This is a useful supplementary PAIN source.

---

## 7. Cross-Dataset Rule

Different datasets should not be mixed directly at the raw feature level unless they use the same feature definition.

Preferred architecture:

```text
raw source videos
      ↓
SilentSign canonical MediaPipe extractor
      ↓
canonical landmark format
      ↓
normalization
      ↓
training
```

This prevents:

```text
different landmark ordering
different coordinate conventions
different missing-value representation
different feature dimensions
```

---

## 8. Canonical Gloss Naming

All developers must use uppercase canonical gloss IDs.

Correct:

```text
PAIN
DOCTOR
YES
WHERE
```

Incorrect:

```text
pain
Pain
PAIN_SIGN
doctor_sign
```

Recommended `vocabulary.json` initial form:

```json
{
  "version": "0.1.0",
  "signs": [
    "DOCTOR",
    "PATIENT",
    "MEDICINE",
    "SICK",
    "YESTERDAY",
    "BANK",
    "MONEY",
    "YES",
    "NO",
    "WHERE",
    "HELP",
    "PAIN"
  ]
}
```

---

## 9. Training Readiness

### Ready enough for preprocessing/model experiments

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

### Not ready

```text
FEVER
ACCOUNT
FORM
SIGNATURE
WHEN
```

---

## 10. Split Policy

Train/validation/test must be **signer-aware**.

Do not:

```text
randomly split individual videos
```

if the same signer can appear in multiple splits.

Prefer:

```text
Train       → known signer subset
Validation  → separate signer subset
Test        → completely unseen signer(s)
```

### Duplicate prevention

For Rishi's raw/cropped dataset:

```text
pain_001_01.AVI
pain_Crop_001_01.avi
```

must be treated as the **same performance identity**.

They must never be placed on opposite sides of the train/test boundary.

---

## 11. Vocabulary Expansion Strategy

After the bootstrap model works end-to-end:

1. Measure accuracy on the 12-sign set.
2. Fix preprocessing/model issues first.
3. Add high-value signs in small batches.
4. Prefer hospital and bank signs.
5. Re-evaluate held-out-signer accuracy after every expansion.

Potential expansion candidates:

```text
HOSPITAL
OFFICE
FEVER
WHEN
ACCOUNT
FORM
SIGNATURE
ACCIDENT
CALL
```

Only add a sign when training data is credible.

---

## 12. Model Scope Statement

The team should describe the first SilentSign model as:

> A fixed-vocabulary ISL sign recognizer for selected hospital, bank, office, and emergency concepts.

Do not describe it as:

> Full Indian Sign Language translation.

The application may compose recognized glosses into short phrases/sentences, but the recognizer itself remains vocabulary-bounded.

---

## 13. Current Audit Verdict

```text
Bootstrap vocabulary size: 12

Ready:
12 / 12 bootstrap signs have a usable candidate source

Backlog:
FEVER
ACCOUNT
FORM
SIGNATURE
WHEN

Cross-source extraction:
VERIFIED

Final 30–50 sign vocabulary:
NOT YET COMPLETE
```

Phase 1 can proceed while vocabulary expansion remains a later parallel task.

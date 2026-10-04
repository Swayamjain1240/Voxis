# SilentSign — Dataset Sources

## 1. Purpose

This document records every dataset currently considered for SilentSign, what role it plays, which signs were verified, and how it should be used.

The project uses a **multi-source dataset strategy** because no single verified dataset currently covers the complete SilentSign vocabulary.

---

## 2. Dataset Inventory

| ID | Dataset | Primary Role | Current Status |
|---|---|---|---|
| DS-01 | AI4Bharat INCLUDE | Main sign-recognition training source | VERIFIED |
| DS-02 | ISL500 / ISL-DATA | Secondary source, especially PAIN | VERIFIED FOR PAIN |
| DS-03 | `vidit031/isl-isolated-40words` | Secondary source for YES/NO/WHERE/HELP | PARTIALLY VERIFIED |
| DS-04 | Emergency ISL Gesture Dataset (Rishi / VOXIS) | Supplementary source for PAIN/DOCTOR/HELP and emergency vocabulary | AUDITED |
| DS-05 | Custom SilentSign recordings | Fill missing vocabulary later | NOT STARTED |

---

## 3. DS-01 — AI4Bharat INCLUDE

### Source

- Dataset: **INCLUDE**
- Organization: AI4Bharat
- Hugging Face dataset: `ai4bharat/INCLUDE`
- Raw archive source: Zenodo record `4010759`
- GitHub project: AI4Bharat INCLUDE repository

### Local project role

INCLUDE is currently the main SilentSign source for the first recognition vocabulary.

### Metadata audit performed

Total metadata rows checked:

```text
Train: 3816
Validation: 425
Test: 1009
Total: 5250
```

A label-vs-folder audit found:

```text
TOTAL ROWS: 5250
MISMATCHES: 49
```

Therefore SilentSign must **not** trust metadata blindly.

A clean manifest was created:

```text
include_manifest.csv
```

Result:

```text
Valid rows: 131
Bad rows: 4
```

### Verified usable classes

| Sign | Clean/valid samples |
|---|---:|
| DOCTOR | 14 |
| PATIENT | 14 |
| MEDICINE | 14 |
| SICK | 21 |
| YESTERDAY | 14 |
| BANK | 40 valid |
| MONEY | 14 |

Additional INCLUDE labels observed during discovery:

```text
HOSPITAL
OFFICE
```

These are not currently part of the locked 12-sign bootstrap vocabulary but may be useful during vocabulary expansion.

### Known bad BANK metadata rows

Excluded:

```text
Places/26. University/MVI_3376.MOV
Clothes/41. Shirt/MVI_5019.MOV
Animals/1. Dog/MVI_3060.MOV
Seasons/64. Fall/MVI_5000.MOV
```

### Technical validation

A real DOCTOR video was successfully processed through the SilentSign MediaPipe pipeline:

```text
Source: MVI_5325.MOV
Frames: 46
Pose detected: 46 frames
Left hand detected: 25 frames
Right hand detected: 30 frames
```

This confirms:

```text
INCLUDE video
   ↓
OpenCV
   ↓
MediaPipe
   ↓
SilentSign landmark JSON
```

---

## 4. DS-02 — ISL500 / ISL-DATA

### Source

Hugging Face dataset repository:

```text
ISL500/ISL-DATA
```

### Current SilentSign purpose

Used primarily to strengthen classes missing or weak in INCLUDE.

### PAIN validation

Exact filename matching found:

```text
PAIN exact total matches: 321
MediaPipe landmark files: 155
Users detected: 15
Raw video files found: 11
```

Important:

`321` represents multiple file representations and must **not** be interpreted as 321 independent raw performances.

### Raw PAIN videos found

Examples:

```text
Videos/User001/Pain__session102__clip019.mp4
Videos/User002/Pain__session177__clip027.mp4
Videos/User003/Pain__session16__clip012.mp4
...
```

### SilentSign extraction tests

#### User001

```text
Frames: 175
Left hand frames: 56
Right hand frames: 0
Pose frames: 175
```

#### User002

```text
Frames: 78
Left hand frames: 46
Right hand frames: 2
Pose frames: 78
```

Both passed through the same extraction pipeline used for INCLUDE.

### Target lookup results

```text
PAIN       → FOUND
FEVER      → NOT FOUND
ACCOUNT    → NOT FOUND
FORM       → NOT FOUND
SIGNATURE  → NOT FOUND
WHEN       → NOT FOUND
```

---

## 5. DS-03 — `vidit031/isl-isolated-40words`

### Source

Hugging Face dataset repository:

```text
vidit031/isl-isolated-40words
```

### Purpose

Secondary vocabulary coverage.

### Verified useful signs

| Sign | Samples found |
|---|---:|
| YES | 17 |
| NO | 17 |
| WHERE | 17 |
| HELP | 16 |
| WHEN | 2 |

### Interpretation

```text
YES    → usable candidate
NO     → usable candidate
WHERE  → usable candidate
HELP   → usable candidate
WHEN   → weak / insufficient by itself
```

### Provenance note

The dataset contains clips originating from multiple upstream sources such as:

```text
ISL500
INCLUDE
CISLR
ISLRTC dictionary
```

Therefore **license/provenance must be tracked per clip**, not assumed from the wrapper dataset as a whole.

### Technical validation

A YES sample was downloaded and processed through the same SilentSign MediaPipe extraction pipeline:

```text
Video: yes__ISL500__00106__Yes__session105__clip014.mp4
Frames: 163
Left hand frames: 49
Right hand frames: 0
Pose frames: 163
```

---

## 6. DS-04 — Emergency ISL Gesture Dataset / VOXIS Audit

### Dataset description

Rishi audited a dataset named:

```text
A Video Dataset of the Hand Gestures of Indian Sign Language Words used in Emergency Situations
```

Local audit root:

```text
D:\VOXIS
```

### Unique signs

```text
ACCIDENT
CALL
DOCTOR
HELP
HOT
LOSE
PAIN
THIEF
```

### Totals

```text
Unique signs: 8
Raw videos: 412
Cropped videos: 412
Total representations: 824
Unique participants: up to 26
```

Important:

Raw and cropped files are **two representations of the same underlying performances**. They must not be counted as independent samples during train/test splitting.

### Strong classes

#### PAIN

```text
52 cropped videos
26 participants
30 FPS
66–118 frames
Average frames: 79.35
Video read errors: 0
```

#### DOCTOR

```text
52 cropped videos
26 participants in detailed analyzer
30 FPS
50–132 frames
Average frames: 89.35
Video read errors: 0
```

#### HELP

```text
52 cropped videos
26 participants
30 FPS
65–101 frames
Average frames: 78.77
Video read errors: 0
```

### Missing target signs

```text
ACCOUNT
FEVER
FORM
NO
SIGNATURE
WHEN
WHERE
YES
```

### Project role

Use this dataset as a **supplementary source**, especially for:

```text
PAIN
DOCTOR
HELP
```

It can also support Rishi's avatar pipeline before Swayam shares selected motion data in Phase 4.

---

## 7. DS-05 — Custom SilentSign Recordings

### Status

```text
NOT STARTED
```

### Purpose

Fill vocabulary gaps that remain after public-dataset search.

Current unresolved examples include:

```text
FEVER
ACCOUNT
FORM
SIGNATURE
WHEN
```

### Recording policy

If custom collection becomes necessary:

- verify the intended ISL sign from a reliable reference or fluent signer
- record several people
- vary lighting and distance
- target roughly 20–30 clips/sign as a starting point
- preserve participant IDs
- obtain appropriate consent/permission
- keep train/test participant separation possible

Do **not** invent signs.

---

## 8. Unified Data Strategy

All recognition-training videos should ultimately pass through one canonical feature pipeline:

```text
INCLUDE ─────┐
ISL500 ──────┤
40-word ─────┼──→ SilentSign MediaPipe extractor
VOXIS ───────┤
Custom ──────┘
                    ↓
              common landmarks
                    ↓
               preprocessing
                    ↓
                  model
```

Do not directly mix incompatible precomputed feature formats unless they have been validated to be equivalent.

---

## 9. Git Policy

Large datasets must remain outside the repository.

Allowed in Git:

```text
data/manifests/
data/samples/        # only if redistribution is permitted
docs/datasets/
scripts/
```

Do not commit:

```text
*.zip
full datasets
multi-GB videos
training caches
private participant data
large model checkpoints
```

---

## 10. Current Decision

The bootstrap recognition vocabulary can proceed using the currently validated multi-source dataset pool.

Dataset expansion continues later, but it does not block Phase 1.

# SilentSign — Phase 0: Dataset & Vocabulary

## Status

**Current status: Conditional Pass / Completed enough to proceed**

Phase 0 establishes the data foundation for both SilentSign directions before application development begins.

---

## 1. Objective

Create a trustworthy initial ISL vocabulary and validate that real dataset videos can be converted into a common landmark representation.

Phase 0 does **not** train the final model.

---

## 2. Swayam Responsibilities

### Dataset discovery and audit
- Audit AI4Bharat INCLUDE.
- Audit ISL500 / ISL-DATA.
- Audit secondary ISL datasets.
- Validate exact sign labels.
- Detect label/path mismatches.
- Create clean manifests.
- Verify raw videos manually.
- Test MediaPipe extraction on real samples.

### Current verified sources
- INCLUDE
- ISL500
- 40-word secondary dataset

### Current bootstrap vocabulary
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

---

## 3. Rishi Responsibilities

- Audit emergency/secondary ISL dataset.
- Validate sign list.
- Count participants and videos.
- Check raw/cropped duplication.
- Identify avatar-useful signs.
- Verify video readability.

Current useful signs include:

```text
PAIN
DOCTOR
HELP
```

---

## 4. Shared Responsibilities

Create and maintain:

```text
shared/vocabulary/vocabulary.json
shared/vocabulary/label_map.json
docs/datasets/sources.md
docs/datasets/licenses.md
docs/datasets/vocabulary-audit.md
```

---

## 5. Phase 0 Deliverables

- Dataset source registry
- Clean INCLUDE manifest
- Secondary source audit
- Initial shared vocabulary
- Consistent gloss naming
- Verified MediaPipe extraction
- Dataset licensing backlog
- Known missing signs list

---

## 6. Known Backlog

```text
FEVER
ACCOUNT
FORM
SIGNATURE
WHEN
```

These do not block Phase 1.

---

## 7. Definition of Done

Phase 0 is considered complete enough when:

- [x] At least one major dataset is audited.
- [x] Initial vocabulary is defined.
- [x] Real videos open successfully.
- [x] MediaPipe extraction works.
- [x] Multiple sources can pass through one extraction pipeline.
- [x] Bad metadata is identified.
- [x] Dataset documentation exists.
- [ ] Final license verification is complete.
- [ ] Final 30–50 sign vocabulary is complete.

---

## 8. Exit Criteria

Proceed to Phase 1 when both developers can work without waiting for additional dataset discovery.

**Decision: GO to Phase 1.**

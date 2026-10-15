# Fixing Part 3 — ML contracts and dataset integrity

## Scope

Fixing Part 3 corrects the sign-recognition foundation before any training or
accuracy claim. It covers canonical preprocessing, the shared 12-gloss label
map, signer-aware manifest validation, duplicate-group isolation, strict
60-frame/300-feature input validation, rejection behavior, and versioned model
metadata.

It does not claim a trained model, dataset accuracy, Whisper, an LLM, TTS,
real avatar clips, or a complete camera-to-gloss product flow.

## Environment and data boundary

No API key, provider, credential, real dataset, or model artifact is required
for this fixing part. Source datasets and generated sequences remain local and
ignored. A training manifest must contain:

```text
sample_id, sequence_path, label, signer_id
```

Extraction starts from a separate source-video manifest containing:

```text
sample_id, video_path, label, signer_id
```

Successful extraction writes a validated training manifest. Unknown signers,
unknown labels, duplicate paths, duplicate sample IDs, and duplicate
content/source groups crossing signer boundaries are rejected.

## Acceptance criteria

- Shoulder normalization uses the canonical pose indices 53 and 54.
- Invalid landmark gaps are interpolated before unrecoverable values are
  zero-filled.
- Training, evaluation, export, and inference use the shared ordered label map
  and `unknown_label = -1`.
- Dataset sequences are exactly `60 × 300` and contain only finite values.
- Signer-wise splits reject duplicate content/source groups crossing boundaries.
- Inference rejects malformed input and unsupported, unknown, or low-confidence
  predictions instead of presenting them as reliable glosses.
- Checkpoints carry and validate model, vocabulary, preprocessing, shape, and
  unknown-label metadata.
- Dataset extraction produces a training-ready manifest.
- No trained-model or accuracy claim is made without the ML runtime, data, and
  held-out-signer evaluation evidence.

## Implementation checkpoints

Part 3 is being delivered as coherent pushed checkpoints on `Swayam`:

1. `837cbd2` — correct landmark preprocessing and regression tests;
2. `ee267cf` — enforce canonical label mapping in training;
3. `c1caa16` — track the manifest validator and duplicate-group safeguards;
4. `ef378b7` — add strict inference input and rejection contracts;
5. `5ebd40f` — version checkpoint metadata across training/evaluation/export;
6. `cfdc63b` — harden extraction, sequence loading, and output manifests;
7. `7fe2025` — document the dataset contract and verification evidence;
8. final verification and Duck review.

## Verification at the current checkpoint

The focused, dependency-light ML checks pass:

```text
20 passed
```

The ML source compiles with `python -m compileall -q src tests`, and
`git diff --check` is clean. The full ML test suite remains environment-gated:
the current Python environment does not have PyTorch, so model test collection
fails with `ModuleNotFoundError: No module named 'torch'`. No training or
accuracy result is reported from this checkout.

Part 3 remains in progress until the final verification and Duck review are
recorded below.

## Final Duck review — Fixing Part 3

**Verdict: DUCK PASS WITH GAPS.**

The Part 3 foundation now has a single canonical contract from preprocessing
through extraction, manifests, signer-wise splitting, training metadata,
evaluation, export, and inference boundaries. Shoulder normalization uses the
correct pose indices; temporal gaps are interpolated before fallback filling;
labels and the `UNKNOWN` value are loaded from the shared vocabulary; malformed
or nonfinite 60×300 sequences are rejected; duplicate source groups cannot
cross signer or split boundaries; and unsupported or low-confidence inference
does not become an accepted gloss.

The extraction tool now distinguishes its source-video manifest from the
training manifest and writes the latter only for successful sequences. Model
metadata records the model, vocabulary, preprocessing, shape, and unknown-label
versions. No API key, provider, credential, real dataset, trained model, or
accuracy claim was introduced.

Evidence for this review:

- focused ML contract/preprocessing/manifest/inference/metadata tests: **20 passed**;
- ML source and scripts: `python -m compileall -q src tests scripts` passed;
- backend regression suite: **98 passed**;
- frontend Vitest: **18 passed**;
- frontend Vite build: completed with the existing React Router directive and
  large-chunk warnings;
- `git diff --check`: clean;
- remote `Swayam` contains all eight Part 3 checkpoints after this review.

The full ML suite remains blocked by the available environment: collecting
`tests/test_models.py` raises `ModuleNotFoundError: No module named 'torch'`.
There is no real dataset or trained checkpoint in this checkout, so held-out
signer accuracy, confusion matrices, latency, model export execution, and
browser camera-to-model behavior were not claimed. MediaPipe assets, Whisper,
LLM/TTS, real avatar clips, and the complete end-to-end translation flows
remain later work.

**Fixing Part 3 is complete for its defined contract-correction scope. Stop
here and wait for the user's explicit command before starting the next part.**

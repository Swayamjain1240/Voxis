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
7. current documentation and dataset-verifier checkpoint;
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

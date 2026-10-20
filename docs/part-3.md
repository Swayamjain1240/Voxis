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

- [x] Shoulder normalization uses the canonical pose indices 53 and 54.
- [x] Invalid landmark gaps are interpolated before unrecoverable values are
  zero-filled.
- [x] Training, evaluation, export, and inference use the shared ordered label
  map and `unknown_label = -1`.
- [x] Dataset sequences are exactly `60 × 300` and contain only finite values.
- [x] Signer-wise splits reject duplicate content/source groups crossing
  boundaries.
- [x] Inference rejects malformed input and unsupported, unknown, or
  low-confidence predictions instead of presenting them as reliable glosses.
- [x] Checkpoints carry and validate model, vocabulary, preprocessing, shape,
  and unknown-label metadata.
- [x] Dataset extraction produces a training-ready manifest.
- [x] No trained-model or accuracy claim is made without the ML runtime, data,
  and held-out-signer evaluation evidence.

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

## Final verification before Duck review

The current branch passes the implementation and contract checks:

```text
52 passed, 2 skipped
```

The ML source compiles with `python -m compileall -q src tests scripts`, and
`git diff --check` is clean. The two skipped tests are the PyTorch-dependent
architecture checks; the suite now skips them explicitly when PyTorch is not
installed instead of failing during collection. No training or accuracy result
is reported from this checkout.

Additional current evidence:

- backend regression suite: **108 passed**;
- frontend Vitest suite: **26 passed**;
- frontend Vite production build: completed with the existing module-directive
  and large-chunk warnings;
- shared vocabulary freeze hashes: verified;
- avatar coverage audit: **0 of 12** approved clips available, with all 12
  canonical glosses reported missing;
- working tree: clean after the completion commit.

The Part 3 implementation and final verification are complete for the defined
ML-contract and dataset-integrity scope. A real dataset, trained checkpoint,
held-out-signer result, and avatar clips remain explicitly outside this
contract-correction scope and are not claimed.

## Duck review — pending

The Duck review is the next required step after this completion checkpoint.

**Not yet recorded.**

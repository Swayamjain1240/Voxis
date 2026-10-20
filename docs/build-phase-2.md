# Build Phase 2 — Data and speech preparation

## Result

Build Phase 2 delivers the preparation layer for both directions:

```text
landmark arrays → validated preprocessing → processed tensors → signer splits
microphone Blob → bounded audio checks → optional local Whisper → transcript
```

The implementation is source-complete for this scope. A real dataset and local
Whisper model remain external runtime inputs and are not committed to the
repository.

## Five pushed checkpoints

1. `1fdaf24` — versioned preprocessing config, finite shape checks, and seeded
   augmentation;
2. `7cbb203` — manifest-driven sequence preparation, path safety, and stable
   per-sample seeds;
3. `9d9351f` — duration/quality metadata and short/silent transcription guards;
4. `ad4b990` — lazy local faster-whisper adapter, structured English response,
   frontend transcription/retry flow, and optional runtime requirements;
5. final signer-split artifacts, invalid-sequence reports, documentation, and
   Duck review.

Every checkpoint is pushed directly to `main`.

## ML/data behavior

`ml/sign-recognition/scripts/prepare_dataset.py` accepts either a validated
manifest or a `label/signer/sample.npy` directory. It writes:

- processed `60 × 300` finite tensors;
- `manifest.csv`;
- `rejected.csv` with sample-level failure reasons;
- `preprocessing_config.json` with version and augmentation settings.

`ml/sign-recognition/scripts/build_splits.py` creates:

```text
train.csv
validation.csv
test.csv
split_metadata.json
```

with signer-isolated train/validation/test groups and duplicate protections.

## Speech behavior

The backend now classifies decodable WAV uploads as `ok`, `too_short`, or
`silent`, reports compressed-format quality as `unknown` when no decoder is
available, and rejects unusable audio at the transcription boundary. The
optional local `faster-whisper` adapter writes no persistent audio files; it
uses a temporary file for the model call and removes it afterward. Missing
runtime/model errors return the existing safe unavailable-service envelope.

The Home page exposes transcription and retry controls. It shows the returned
English transcript only when the backend returns one; it does not fabricate
text while Whisper is disabled or unavailable.

## Evidence and remaining runtime setup

- focused ML tests: **26 passed**;
- backend tests: **102 passed**;
- frontend tests: **26 passed**;
- frontend build: passed with existing Vite module-directive and chunk-size
  warnings;
- ML source/scripts compilation: passed;
- `git diff --check`: clean.

The optional package is listed in `backend/requirements-speech.txt`. A local
model and a real spoken-sentence run are still required before claiming runtime
transcription accuracy. This is the final Phase 2 checkpoint; the next phase
does not start automatically.

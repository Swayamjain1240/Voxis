# VOXIS — AI-Assisted Indian Sign Language Communication

> **From silence to speech. From speech to sign.**

VOXIS is the public product name for this project. Older planning material and
some source comments may still use **SilentSign**; that name is historical and
is retained only where it helps explain repository history or compatibility.

## Current status at a glance

This repository is at the **Phase 1 foundation** stage. It is not yet a
complete two-way sign-language translator. The current source supports the
local microphone/avatar foundation and an asset-gated camera-to-sequence input
foundation; the end-to-end AI pipelines are still planned work.

The status labels used in this README and the phase/architecture documents are:

| Status | Meaning |
| --- | --- |
| **Implemented (source)** | The repository contains an implementation for the described foundation behavior. This label is source-based; it is not a claim that a build or test run was performed for this documentation update. |
| **Partial / scaffold** | A component, contract, or boundary exists, but the user-visible or end-to-end behavior is not complete. |
| **Planned** | The behavior is documented as a future phase and is not available as a complete flow now. |
| **Deferred / not applicable** | Deliberately outside the current Phase 1 scope, including Mode 2 and production-only controls. |

### Phase 1 foundation status

| Area | Current status | What is true today |
| --- | --- | --- |
| Frontend shell and routes | **Implemented (source)** | React/Vite pages for Home, Conversation, and Debug are present. |
| Microphone foundation | **Implemented (source)** | The Home page requests microphone permission, records with `MediaRecorder`, stops tracks, and offers a local audio preview/blob. |
| Avatar foundation | **Implemented (source)** | A procedural Three.js avatar renders idle/wave/sign gestures. An optional GLB URL boundary exists, but a production sign-animation library is not present. |
| Camera/sign input | **Implemented (source, asset-gated)** | The Conversation route requests camera permission, shows local video and landmarks, runs the configured MediaPipe Holistic Landmarker adapter, buffers a validated 60-frame canonical sequence, and offers local JSON export. Model/WASM asset paths are optional and the sign model is not enabled. |
| Backend foundation | **Partial / scaffold** | FastAPI health/readiness routes, exact host/origin policy, bounded/content-validated audio upload, typed REST models, request limits, security headers, and an explicitly disabled WebSocket boundary exist. They do not constitute the completed translation pipelines. |
| Speech recognition | **Planned** | Whisper/faster-whisper is represented by a disabled service boundary. Audio capture/upload is not transcription. |
| Sign recognition | **Planned** | ML extraction/preprocessing/model helpers and a disabled backend inference boundary exist, but no trained or loaded model is part of the current runtime. |
| Language and speech output | **Partial / scaffold** | A deterministic, vocabulary-constrained keyword/template fallback exists. LLM-backed conversion and TTS are not integrated. |
| Conversation experience | **Partial / scaffold** | Context selection, turn state, transcript/gloss display, clear/reset, camera foundation, and honest microphone/upload states are connected; translation directions are not end to end. |
| Remote communication | **Deferred / not applicable** | Mode 2 rooms, QR/room joining, and remote media/landmark exchange are deliberately disabled. |

**Overall Phase 1 status: source foundation implemented / runtime verification
pending.** The speech/avatar slice is usable as a foundation demo and the
`camera → live landmarks → buffered sequence` flow is wired in the Conversation
route. A live browser run still requires local public MediaPipe assets and
manual/E2E verification. See [`docs/phases/phase-1.md`](docs/phases/phase-1.md)
for the detailed evidence-based status.

## Fixed-vocabulary limitation

The current shared contract contains **12 uppercase gloss labels**:

```text
DOCTOR  PATIENT  MEDICINE  SICK  YESTERDAY  BANK
MONEY   YES      NO        WHERE HELP       PAIN
```

This is a restricted bootstrap vocabulary, not a 30–50 sign implementation and
not unrestricted continuous Indian Sign Language translation. The intended
near-term behavior is isolated signs and short, supported phrases. Unsupported
or uncertain input must remain visible as unsupported/uncertain; it must not be
silently presented as a reliable translation. Vocabulary expansion requires
new data, licensing review, signer-aware evaluation, and updated animation or
language mappings.

The decision is recorded in
[`docs/decisions/ADR-003-fixed-vocabulary-mvp.md`](docs/decisions/ADR-003-fixed-vocabulary-mvp.md)
and the current audit is in
[`docs/datasets/vocabulary-audit.md`](docs/datasets/vocabulary-audit.md).

## Product direction and use cases

VOXIS is intended to help an Indian Sign Language user and a non-signer have a
face-to-face conversation using an ordinary camera, microphone, and screen. It
is an assistive communication prototype for situations where an interpreter is
not immediately available; it does not replace a qualified interpreter or
professional judgment.

The first product direction is **Mode 1**, one phone or laptop placed between
two people:

```text
Signer → camera → supported sign/gloss → text and optional speech
Speaker → microphone → transcript → restricted glosses → signing avatar
```

The intended settings include hospitals, banks, government or public-service
counters, reception desks, and other short, privacy-sensitive interactions.
Examples such as a patient communicating `PAIN` or `MEDICINE`, or a customer
asking a supported `MONEY` or `BANK` question, describe the target vocabulary
experience. They are not evidence that the current checkout recognizes those
sentences end to end.

### Sign → text/speech direction

The planned pipeline is:

```text
Camera → browser MediaPipe landmarks → 60-frame sequence
       → fixed-vocabulary sign model → glosses → restricted language output
       → captions and optional speech
```

Camera lifecycle helpers, landmark contracts, a configured Tasks Vision adapter,
a bounded capture loop, user-facing states, and local sequence export are
present in the Conversation route. A trained sign model, confidence policy,
and complete translation route are still planned.

### Speech → transcript → signing avatar direction

The planned pipeline is:

```text
Microphone → bounded audio request → Whisper transcript
           → restricted gloss/template conversion → animation lookup → avatar
```

The current Home page demonstrates local microphone capture and a procedural
avatar. Whisper, LLM conversion, TTS, and a real sign-animation library are
explicitly disabled or planned; audio capture is not transcription.

### Mode 2 is a later extension

Remote rooms, QR codes, two-device exchange, and remote landmark/media
transport remain future scope. The current `/ws` route is deliberately closed,
and the frontend does not open a browser socket. A future Mode 2 implementation
must add identity, room/resource authorization, validated events, isolation,
limits, and a privacy review before it is enabled.

## Privacy-oriented design

Raw camera video is intended to stay in the browser where possible. When speech
transcription is enabled in a later phase, the client should send only the
bounded audio needed for the active request; the current backend does not
persist uploads or conversation history. Browser permission prompts, track
cleanup, explicit service failures, and a local clear/reset path are part of
the foundation, while the complete privacy/retention policy remains future work.

## Intended conversation journey

The target user journey is:

```text
Open VOXIS
  ↓
Choose a supported context (hospital, bank, office)
  ↓
Review camera/microphone permissions and readiness
  ↓
Use the one-device conversation view
  ↓
See supported glosses, captions, uncertainty, or a clear unavailable state
  ↓
Clear the local session when finished
```

The current routes provide the application shell, Home microphone/avatar
foundation, a Conversation foundation screen, and Debug surface. The complete
camera-to-gloss and speech-to-avatar journey is not connected yet.

## Demonstration scenario (target, not current capability)

A future hospital demonstration may show a signer selecting the hospital
context and producing a supported sequence such as `YESTERDAY`, `DOCTOR`, or
`PAIN`; the hearing user can then speak a short supported response and review
the transcript/glosses before the avatar plays available clips. Every demo
should show the fixed vocabulary, uncertainty, and service-disabled states.
No README example should be interpreted as an accuracy result or as a claim of
continuous free-form ISL translation.

## Design principles

- **Two-way direction:** Sign → text/speech and speech → transcript/gloss/avatar
  are separate pipelines with explicit failure states.
- **No special hardware:** the target uses ordinary cameras, microphones, and a
  display.
- **Restricted before broad:** reliability, evaluation, licensing, and
  user-visible uncertainty come before vocabulary expansion.
- **Privacy by design:** keep raw media local where possible and avoid default
  persistence.
- **Evidence-based claims:** source scaffolding, a demo placeholder, and a
  service boundary are not the same as a trained or deployed model.

## What is currently in the repository

### Implemented or source-backed foundation

- `frontend/` contains the React/Vite application shell, local microphone
  capture, audio preview, procedural avatar rendering, debug/status surfaces,
  and reusable camera/sign-input utilities.
- `backend/` contains a FastAPI application with health/liveness/readiness,
  development configuration, content-validated audio upload, typed contracts,
  bounded HTTP safeguards, and an explicitly disabled WebSocket boundary.
- `shared/vocabulary/` contains the versioned 12-gloss bootstrap vocabulary,
  label map, and context allowlists.
- `shared/contracts/` contains JSON schemas for the planned cross-service
  messages.
- `ml/sign-recognition/` contains extraction, preprocessing, model, evaluation,
  inference, and export modules as development scaffolding. Source modules are
  not evidence of a trained, evaluated, or deployed model.

### Not yet a complete product flow

The following are not currently connected into a verified end-to-end path:

```text
camera → browser MediaPipe → landmarks → trained sign model
      → gloss sequence → language conversion → text/TTS

microphone → Whisper → supported glosses → real sign clips → avatar
```

The current conversation page says that the conversation engine is not
connected. The current backend reports Whisper and sign-model features as
disabled by default. Those explicit runtime boundaries are the authoritative
status for this checkout.

## Architecture boundary

The target architecture is intentionally split into independent layers:

```text
Browser camera/microphone
        ↓
Frontend capture and privacy boundary
        ↓
FastAPI REST contracts (future Mode 2 WebSocket design)
        ↓
Optional speech/language/TTS services
        ↓
Sign model runtime and shared vocabulary
        ↓
Captions, audio, and avatar presentation
```

For the current implementation, raw camera video is intended to remain in the
browser where possible. Microphone audio may be uploaded for a bounded
transcription request once that service is enabled. No database-backed user
history, account system, administrator console, or production deployment is
part of Phase 1.

See [`docs/architecture/system-architecture.md`](docs/architecture/system-architecture.md),
[`docs/architecture/sign-to-speech.md`](docs/architecture/sign-to-speech.md),
and [`docs/architecture/speech-to-sign.md`](docs/architecture/speech-to-sign.md)
for target flows and their current-state notes.

## Local environment files

Backend and frontend configuration stay separate:

```text
backend/.env   # FastAPI-only settings
frontend/.env  # Vite/browser-only public settings
```

Copy the committed `.env.example` in each directory when setting up locally.
Actual `.env` files are ignored and must never be committed. Current VOXIS work
does not require an API key. Optional MediaPipe model/WASM asset paths are
public local asset settings, not secrets. See [`docs/environment.md`](docs/environment.md).

## Repository map

```text
VOXIS/
├── frontend/                 # React/Vite UI and browser capture boundaries
├── backend/                  # FastAPI contracts and runtime boundaries
├── ml/                       # Offline sign-recognition development code
├── shared/                   # Vocabulary, labels, and JSON contracts
├── docs/                     # Status, phases, architecture, API, and data notes
└── .gitignore
```

Large source datasets and generated model artifacts are intentionally not
treated as product features merely because a directory or placeholder exists.
Dataset provenance and licensing remain an open part of the data work.

## Roadmap and scope

| Phase | Status | Scope |
| --- | --- | --- |
| Phase 0 — Dataset and vocabulary | **Conditional foundation** | Audit notes and the 12-label shared vocabulary exist; final license verification and the later 30–50 target remain open. |
| Phase 1 — Input foundation | **Source foundation implemented / runtime verification pending** | Microphone capture, procedural avatar rendering, and the asset-gated browser camera-to-landmark sequence path are source-backed; trained inference and complete translation remain later work. |
| Phase 2 — Data and speech preparation | **Planned** | Reproducible preprocessing, signer-aware manifests, and real Whisper transcription. |
| Phase 3 — AI core | **Planned** | Trained/evaluated fixed-vocabulary model and restricted language conversion. |
| Phase 4 — Live recognition and avatar clips | **Planned** | Runtime model loading, confidence/rejection behavior, and real sign animation assets. |
| Phase 5 — Complete pipelines | **Planned** | Independently working sign-to-speech and speech-to-sign flows. |
| Phase 6 — Integration and reliability | **Planned** | One-device Mode 1 conversation, error handling, release evidence, and security hardening. |
| Mode 2 — Remote communication | **Deferred** | Rooms, QR codes, remote exchange, and related authorization are not Phase 1 requirements. |

Feature ideas such as unrestricted continuous ISL translation, a larger
vocabulary, Hindi expansion, fingerspelling, facial-expression recognition,
offline/mobile operation, accounts, and friends/contacts remain future scope.

## Security and privacy status

The current security posture is a development/Phase 1 baseline, not a
production security claim. Current source-backed controls include browser media
permission flows, bounded/content-validated audio upload, environment-based
feature flags/configuration, exact development CORS origins and hosts, typed
request models, request limits/timeouts, security response headers, and a
deliberately no-login Mode 1 boundary. Production TLS, authentication,
database controls, backups, administration, monitoring, and release security
review are future or not applicable to this foundation. The full register is in
[`docs/security-threat-model.md`](docs/security-threat-model.md).

## Verification note

The current checkpoint has been verified with `backend/.venv/Scripts/python.exe
-B -m pytest -p no:cacheprovider` (**98 passed**) and `npm test -- --run`
(**25 passed**). `npm run build` also completed; Vite reported its existing
module-directive and large-chunk warnings. Earlier dependency checks recorded
clean `pip check`, `pip-audit`, and npm audit results. These checks do not prove
translation accuracy, latency, privacy compliance, penetration resistance,
browser E2E behavior, or production readiness.

## Responsible-use note

VOXIS should be presented according to measured capabilities. It is an
assistive communication prototype, not a substitute for a qualified interpreter
or professional judgment. In sensitive contexts such as healthcare, show the
supported glosses, uncertainty, and limitations clearly; do not claim that a
fixed-vocabulary prototype understands unrestricted conversation.

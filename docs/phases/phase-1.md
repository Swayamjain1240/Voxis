# SilentSign — Phase 1: Input Foundation

## Objective

Make both input sides of SilentSign work independently.

No model training in this phase.

---

## 1. Swayam — Sign Input Foundation

Build:

```text
Browser Camera
   ↓
Live Video
   ↓
MediaPipe
   ↓
Hand + Pose Landmarks
   ↓
Landmark Overlay
   ↓
Canonical Landmark Frame
   ↓
30–60 Frame Buffer
```

### Tasks

- [ ] Camera permission flow
- [ ] Camera stream lifecycle
- [ ] Camera cleanup
- [ ] MediaPipe setup in browser
- [ ] Left-hand landmarks
- [ ] Right-hand landmarks
- [ ] Pose landmarks
- [ ] Landmark overlay
- [ ] Convert landmarks to canonical numeric structure
- [ ] Create sliding frame buffer
- [ ] Save/debug one live landmark sequence
- [ ] Handle no-camera / permission errors

### Frontend ownership

```text
frontend/src/features/sign-input/
```

---

## 2. Rishi — Speech/Avatar Foundation

Build:

```text
Microphone
   ↓
Audio Capture

and

3D Avatar
   ↓
Browser Render
   ↓
Basic Idle / Test Animation
```

### Tasks

- [ ] Microphone permission
- [ ] Start/stop recording
- [ ] Audio status
- [ ] Optional basic waveform
- [ ] Audio cleanup
- [ ] React Three Fiber / Three.js setup
- [ ] Load rigged GLB avatar
- [ ] Render avatar
- [ ] Run one basic animation
- [ ] Handle mic/avatar loading errors

### Frontend ownership

```text
frontend/src/features/speech-input/
frontend/src/features/avatar/
```

---

## 3. Shared Contract

Both developers must use shared canonical labels and types.

No arbitrary label names.

Example:

```text
PAIN
DOCTOR
HELP
```

---

## 4. Git Workflow

```text
main
├── swayam
└── rishi
```

Rules:
- Develop only on personal branch.
- Push working commits to personal branch.
- Merge tested work into `main`.
- Pull latest `main` after the other developer merges shared changes.

---

## 5. Phase 1 Deliverables

### Swayam
- Live camera
- MediaPipe landmarks
- Visible landmark overlay
- Canonical frame structure
- Frame buffer

### Rishi
- Working microphone capture
- Working avatar render
- Basic avatar animation

---

## 6. Definition of Done

Phase 1 passes when:

```text
Swayam:
camera → live landmarks → buffered sequence

Rishi:
microphone works + avatar loads and moves
```

Neither pipeline depends on the other.

---

## 7. Do Not Do Yet

- No Transformer training
- No Whisper integration
- No LLM integration
- No final avatar sign library
- No Mode 2
- No authentication

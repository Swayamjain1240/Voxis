# SilentSign — Phase 4: Real-Time Recognition & Avatar

## Objective

Turn the AI core into real-time user-facing behavior.

---

## 1. Swayam — Live Sign Recognition

Flow:

```text
Camera
   ↓
MediaPipe
   ↓
Sliding Window
   ↓
Preprocessing
   ↓
Classifier
   ↓
Post-processing
   ↓
Stable Gloss Output
```

### Tasks

- [ ] Load trained model in runtime
- [ ] Run inference on live frame windows
- [ ] Match training preprocessing exactly
- [ ] Prediction smoothing
- [ ] Duplicate suppression
- [ ] Confidence threshold
- [ ] UNKNOWN rejection
- [ ] Top-3 alternatives
- [ ] Sign start/end detection
- [ ] Manual Done fallback
- [ ] Build gloss sequence
- [ ] Measure latency

---

## 2. Rishi — Avatar Sign Library

Flow:

```text
Gloss
   ↓
Animation Registry
   ↓
Motion Clip
   ↓
Avatar
```

### Initial source

Rishi may begin with his own validated data for:

```text
PAIN
DOCTOR
HELP
```

### Dataset handoff point

At this phase Swayam shares selected approved reference data for missing signs.

Possible shared package:

```text
avatar_reference/
├── YES/
├── NO/
├── WHERE/
├── MEDICINE/
└── YESTERDAY/
```

Share only what is needed and only if license terms permit.

### Tasks

- [ ] Create animation registry
- [ ] Build first real sign clip
- [ ] Retarget motion to avatar
- [ ] Sequential playback
- [ ] Animation blending
- [ ] Caption synchronization
- [ ] Replay
- [ ] Slow playback
- [ ] Missing-animation fallback

---

## 3. Phase 4 Deliverables

### Swayam
Real-time:

```text
camera → stable gloss
```

### Rishi
Real:

```text
gloss → avatar sign
```

---

## 4. Definition of Done

Phase 4 passes when:

- [ ] Swayam can perform known signs live and receive stable predictions.
- [ ] Low-confidence input is rejected safely.
- [ ] Duplicate predictions are controlled.
- [ ] Rishi can play multiple real sign animations.
- [ ] Captions follow animation playback.
- [ ] Missing sign clips have a safe fallback.

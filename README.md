
# 🖤 VOXIS — AI-Powered Sign Language Communication

> **From silence to speech. From speech to sign.**

VOXIS is an AI-powered, real-time two-way communication system designed to bridge the communication gap between **Indian Sign Language (ISL) users and non-signers**.

VOXIS converts **sign language → text + speech** and **speech → text + visual signing through a 3D avatar**, enabling more natural conversations without requiring a human interpreter.

---

## 🚀 Why VOXIS?

Millions of deaf and hard-of-hearing people face communication barriers in places such as:

* 🏥 Hospitals
* 🏦 Banks
* 🏢 Government offices
* 🏨 Reception desks
* 📞 Remote communication

Human interpreters are not always available, while writing or relying on relatives can be slow and reduce privacy.

**VOXIS aims to provide an always-available AI communication bridge using only a regular camera and microphone.**

---

## ✨ Core Features

### 🤟 Sign → Speech

The camera captures the user's signing and the AI pipeline:

```text
Camera
   ↓
MediaPipe Holistic
   ↓
Landmark Extraction
   ↓
Transformer / Conformer
   ↓
Sign / Gloss Recognition
   ↓
LLM Grammar Processing
   ↓
Text + Speech
```

Example:

```text
User signs:
ME → STOMACH → PAIN

VOXIS outputs:
"I have a stomach ache."
```

---

### 🎙️ Speech → Sign

The hearing person can speak naturally.

```text
Microphone
    ↓
Whisper
    ↓
Speech → Text
    ↓
LLM
    ↓
Text → ISL Sign Order
    ↓
Sign Animation Lookup
    ↓
3D Avatar
```

The 3D avatar then performs the corresponding signs while captions are displayed.

---

## 🧠 AI Architecture

VOXIS combines multiple AI components instead of relying on a single model.

### 1. Computer Vision

**MediaPipe Holistic** detects hand, body and facial landmarks from the camera stream.

Approximately **540 key points** can be extracted from each frame.

The landmarks are normalized using shoulder position and shoulder width to reduce the effect of camera distance and body size.

---

### 2. Sign Recognition

A sequence of landmark frames is passed into a:

* Transformer
* or Conformer

The model predicts a sign label, also called a **gloss**.

Example:

```text
PAIN
DOCTOR
WHERE
MEDICINE
YES
NO
```

The initial system focuses on a controlled vocabulary of approximately **30–50 important signs** for reliable hackathon demonstrations.

---

### 3. LLM Language Layer

Sign languages have their own grammar and word order.

VOXIS uses an LLM to convert recognized glosses into natural sentences.

```text
ME STOMACH PAIN
        ↓
"I have a stomach ache."
```

The LLM can also convert spoken sentences into the appropriate sign order.

---

### 4. Speech Recognition

VOXIS uses **Whisper / faster-whisper** for speech-to-text.

Supported speech languages in the planned system include:

* English
* Hindi

---

### 5. Text-to-Speech

The generated sentence can be converted into spoken audio using:

* Edge-TTS
* Google TTS
* AI4Bharat Indic TTS

---

### 6. 3D Signing Avatar

For speech-to-sign communication, VOXIS uses a 3D avatar.

The avatar:

1. Receives the sign sequence.
2. Finds the corresponding animation clips.
3. Plays the clips sequentially.
4. Displays synchronized captions.

The planned implementation uses **Three.js / React Three Fiber** with a rigged 3D model.

---

# 🔄 Two Communication Modes

## Mode 1 — Face-to-Face

The core MVP uses a **single phone or laptop** placed between two people.

```text
        SIGNER
          🤟
           ↓
      📷 CAMERA
           ↓
        VOXIS
       ↙     ↘
    TEXT     SPEECH
             🔊
           PERSON
```

The hearing person can then speak into the microphone.

```text
Speech
   ↓
Whisper
   ↓
Text
   ↓
LLM
   ↓
Sign Order
   ↓
3D Avatar
```

### Best suited for:

* Hospitals
* Banks
* Offices
* Reception desks
* Government kiosks

---

## Mode 2 — Remote Communication

Two devices can communicate through a real-time connection.

```text
Phone A                     Phone B

Deaf User                   Hearing User
   🤟                           🎙️
   ↓                             ↓
Camera                        Microphone
   ↓                             ↓
Landmarks                     Speech
   ↓                             ↓
        WebSocket / Server
                 ↓
              VOXIS AI
                 ↓
        ┌────────┴────────┐
        ↓                 ↓
      Text              Avatar
        ↓                 ↓
     Speech             Signing
```

A **6-digit room code or QR code** can be used to connect the two users.

---

# 🏗️ System Architecture

```text
                         ┌───────────────────┐
                         │      VOXIS        │
                         │ Communication AI  │
                         └─────────┬─────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
              ▼                                         ▼
       SIGN → SPEECH                              SPEECH → SIGN
              │                                         │
         Camera Input                              Microphone
              │                                         │
              ▼                                         ▼
      MediaPipe Holistic                           Whisper
              │                                         │
              ▼                                         ▼
       Landmark Sequence                              Text
              │                                         │
              ▼                                         ▼
    Transformer / Conformer                            LLM
              │                                         │
              ▼                                         ▼
         Sign / Gloss                              ISL Sign Order
              │                                         │
              ▼                                         ▼
             LLM                                  Animation Lookup
              │                                         │
        ┌─────┴─────┐                                    ▼
        ▼           ▼                              3D Avatar
      Text        TTS                                   │
        │           │                                    ▼
        └─────┬─────┘                              Visual Sign
              ▼
          User Output
```

---

# 🛠️ Tech Stack


| Layer                   | Technology                                  |
| ------------------------- | --------------------------------------------- |
| Frontend                | React + Vite                                |
| Styling                 | Tailwind CSS                                |
| Computer Vision         | MediaPipe Holistic                          |
| Sign Recognition        | PyTorch                                     |
| Model Architecture      | Transformer / Conformer                     |
| Model Deployment        | ONNX                                        |
| Backend                 | FastAPI                                     |
| Real-Time Communication | WebSockets                                  |
| Speech Recognition      | Whisper / faster-whisper                    |
| Language Layer          | LLM API                                     |
| Text-to-Speech          | Edge-TTS / Google TTS / AI4Bharat Indic TTS |
| 3D Avatar               | Three.js / React Three Fiber                |
| Animation               | Rigged GLB + animation clips                |
| Optional Authentication | Firebase Auth / Supabase                    |
| Dataset                 | ISL-CSLTR / INCLUDE / Custom recordings     |

---

# 🔐 Privacy by Design

Privacy is an important part of VOXIS.

Instead of continuously transmitting raw video, the system is designed to process video locally and work primarily with extracted landmark data.

```text
Camera Video
     ↓
Local Landmark Extraction
     ↓
Small Numerical Landmark Data
     ↓
AI Processing
```

This approach can provide:

* Reduced bandwidth usage
* Faster processing
* Better privacy
* Less dependence on raw video transmission

Users can also clear the conversation session.

---

# 📊 Data & Model Strategy

VOXIS initially focuses on a controlled vocabulary instead of attempting unrestricted continuous sign-language translation.

### Initial vocabulary

Approximately:

**30–50 signs**

Examples:

### 🏥 Hospital

```text
PAIN
DOCTOR
MEDICINE
FEVER
WHERE
WHEN
YES
NO
```

### 🏦 Bank

```text
ACCOUNT
MONEY
FORM
SIGNATURE
```

### Training Pipeline

```text
ISL Dataset / Custom Recordings
              ↓
       Landmark Extraction
              ↓
         Normalization
              ↓
       Sequence Padding
              ↓
       Data Augmentation
              ↓
     Transformer / Conformer
              ↓
       Model Evaluation
              ↓
             ONNX
              ↓
        Real-Time Inference
```

The model should be evaluated using a **held-out person** who was not included in training data to better test generalization.

---

# 🎯 Target Use Cases

## 🏥 Healthcare

A deaf patient can communicate symptoms to medical staff.

```text
SIGN:
ME → STOMACH → PAIN

VOXIS:
"I have a stomach ache."
```

The doctor can respond verbally and VOXIS can convert the response into visual signing.

---

## 🏦 Banking

VOXIS can assist with basic interactions such as:

* Opening an account
* Forms
* Money-related queries
* Signatures
* Customer support

---

## 🏢 Government & Public Services

VOXIS can provide an accessible communication layer at:

* Government counters
* Public service desks
* Reception areas
* Information kiosks

---

## 📞 Remote Communication

The remote mode can support:

* Telemedicine
* Customer support
* Family conversations
* Remote assistance

---

# 🎨 User Experience

The main interface contains two communication sides.

### Signer Side

* Live camera
* Landmark visualization
* Recognized sign chips
* Confidence score
* Communication status

### Hearing Side

* Microphone
* Audio output
* Live captions
* 3D signing avatar
* Conversation transcript

---

# ⚡ Error Handling

VOXIS includes fallback mechanisms for unreliable AI or environmental conditions.


| Problem             | VOXIS Response                         |
| --------------------- | ---------------------------------------- |
| Hands not detected  | Ask user to show hands                 |
| Poor lighting       | Lighting/framing guidance              |
| Sign not recognized | Ask user to sign again                 |
| Low confidence      | Show alternative predictions           |
| Noisy audio         | Display transcript for confirmation    |
| LLM/network failure | Show raw glosses / quick phrases       |
| Camera blocked      | Explain permission issue               |
| Unknown avatar sign | Display text / optional fingerspelling |

---

# 🛡️ Safety & Reliability

VOXIS is designed to avoid blindly speaking uncertain predictions.

For sensitive environments such as healthcare, the planned system can provide:

### "Did you mean...?"

When confidence is low:

```text
Possible interpretation:

1. PAIN      82%
2. FEVER     11%
3. MEDICINE   7%

        [ CONFIRM ]
        [ TRY AGAIN ]
```

This allows the user to verify important information before it is spoken.

---

# 📱 User Flow

```text
OPEN VOXIS
    ↓
START CONVERSATION
    ↓
Choose Context
    ↓
Hospital / Bank / Office
    ↓
Communication Preferences
    ↓
Camera + Microphone
    ↓
Readiness Check
    ↓
┌─────────────────────────────┐
│                             │
│       Conversation          │
│                             │
│  Sign → Speech              │
│  Speech → Avatar            │
│                             │
└─────────────────────────────┘
    ↓
Conversation Transcript
    ↓
CLEAR SESSION
```

---

# 🧪 MVP Scope

The primary hackathon MVP focuses on:

* [X]  Real-time camera input
* [X]  MediaPipe landmark detection
* [X]  Sign recognition
* [X]  Gloss generation
* [X]  LLM sentence generation
* [X]  Text-to-speech
* [X]  Speech-to-text
* [X]  Speech-to-sign conversion
* [X]  3D signing avatar
* [X]  Captions
* [X]  Conversation transcript
* [X]  Face-to-face mode
* [X]  Session clearing

### Future Scope

* [ ]  Remote room-code communication
* [ ]  QR-based room joining
* [ ]  Hindi + English expansion
* [ ]  Fingerspelling
* [ ]  Facial-expression recognition
* [ ]  Offline/on-device mode
* [ ]  Mobile PWA
* [ ]  User accounts
* [ ]  Friends/contacts
* [ ]  Larger ISL vocabulary
* [ ]  Continuous free-form ISL translation

---

# ⚠️ Current Limitations

VOXIS is initially designed around **isolated signs and short phrases from a fixed vocabulary**.

It is **not intended to claim full free-form continuous Indian Sign Language translation** at this stage.

The initial strategy prioritizes:

> **Reliability → Accuracy → Real-world usefulness → Vocabulary expansion**

rather than attempting to solve unrestricted sign-language translation immediately.

---

# 🚀 Development Roadmap

### Phase 1 — Foundation

* Camera pipeline
* MediaPipe landmarks
* Avatar loading
* Whisper integration
* Vocabulary definition
* Data collection

### Phase 2 — AI Core

* Train sign recognition model
* Build gloss pipeline
* Integrate LLM
* Implement TTS
* Create avatar sign clips

### Phase 3 — Integration

* Connect frontend + backend
* WebSocket pipeline
* Split-screen interface
* Context-specific vocabulary
* Remote room mode

### Phase 4 — Polish

* Debug mode
* Confidence visualization
* Error handling
* Performance optimization
* Demo reliability
* Presentation and documentation

---

# 🧑‍💻 Team Roles

A suggested four-person team structure:


| Role               | Responsibility                                     |
| -------------------- | ---------------------------------------------------- |
| ML Engineer        | Dataset, landmark extraction, model training, ONNX |
| Backend Engineer   | FastAPI, WebSockets, Whisper, LLM, TTS             |
| Frontend Engineer  | React UI, camera, MediaPipe, captions              |
| 3D / Demo Engineer | Three.js avatar, animations, demo and presentation |

---

# 🏆 Hackathon Demo

### 3-Minute Demo Flow

**1. Launch VOXIS**

Select:

```text
🏥 HOSPITAL MODE
```

**2. Patient signs**

```text
ME → STOMACH → PAIN
```

VOXIS generates:

> "I have a stomach ache."

The system displays the sentence and speaks it aloud.

**3. Doctor responds**

Doctor says:

> "Since when?"

VOXIS converts the sentence into sign order and the 3D avatar signs the response.

**4. Patient responds**

```text
YESTERDAY
```

VOXIS responds:

> "Since yesterday."

**5. Switch to Bank Mode**

Demonstrate a banking interaction.

**6. Show Debug Mode**

Display:

* Recognition confidence
* Processing stages
* Latency
* Recognized gloss
* AI pipeline

---

# 💡 What Makes VOXIS Different?

### 🔄 Two-Way Communication

Most basic sign-language projects focus on only:

```text
Sign → Text
```

VOXIS focuses on:

```text
Sign ↔ Speech
```

---

### 📷 No Special Hardware

VOXIS is designed around ordinary:

* Smartphone cameras
* Laptop webcams
* Microphones

---

### 🔐 Privacy-Oriented

The architecture prioritizes local video processing and landmark-based communication rather than transmitting raw video whenever possible.

---

### 🇮🇳 Indian Sign Language Focus

The initial system is specifically designed around **Indian Sign Language** and real-world Indian contexts such as hospitals and banks.

---

### 🧠 Multi-AI Pipeline

VOXIS combines:

```text
Computer Vision
       +
Deep Learning
       +
LLM
       +
Speech AI
       +
3D Animation
```

into a single communication system.

---

# 🌑 VOXIS

> **THE LANGUAGE YOU CAN'T HEAR.**

### Sign → Understand → Speak

### Speak → Understand → Sign

**VOXIS — Making communication accessible through AI.**

---

## 📄 Project Status

🚧 **Build X Hackathon — AI/ML Project**

Current focus:

> Real-time Indian Sign Language communication using computer vision, sequence modeling, LLMs, speech AI, and 3D avatar technology.

---

## ⚖️ Responsible AI Note

VOXIS should be presented according to its measured capabilities. The initial model recognizes a controlled vocabulary of isolated signs and short phrases; accuracy should be reported using actual held-out evaluation results rather than assumed performance.

Before using external datasets, avatar models, or recorded signing data, their licenses and usage terms should be verified.

# VOXIS local environment

VOXIS keeps backend and frontend configuration in separate files:

```text
backend/.env      # FastAPI-only settings
frontend/.env     # Vite/browser-only public settings
```

Start from the committed examples:

```text
backend/.env.example  → backend/.env
frontend/.env.example → frontend/.env
```

Actual `.env` files are ignored by the root, backend, and frontend Git ignore
rules. Only `.env.example` files are allowed to be committed. Never put an API
key, password, private certificate, database credential, or provider secret in a
`VITE_*` variable because Vite exposes those values to the browser bundle.

## Current variables

### Backend

`backend/.env.example` contains the FastAPI host/port, exact CORS origins and
allowed hosts, request limits, upload limit, and disabled feature gates. No API
key is required for the current foundation or Fixing Part 2.

### Frontend

`frontend/.env.example` contains the public API base URL, app name, and optional
local/public asset paths. WebSockets are disabled in Mode 1, so `VITE_WS_URL`
is intentionally not used.

The optional MediaPipe values are:

```text
VITE_MEDIAPIPE_MODEL_URL=/models/hand_landmarker.task
VITE_MEDIAPIPE_WASM_ROOT=/mediapipe/wasm
```

They are asset paths, not credentials. Fixing Part 2 builds and tests without
them; the camera preview then reports that the processor is not configured.
When a compatible model and WASM assets are added under the frontend's public
assets, the same adapter can initialize without a provider API key.

No external API or secret is introduced by this environment contract. If a
future speech, LLM, TTS, hosted model, or analytics provider is added, disclose
the provider, purpose, secret name, and backend location before adding it.

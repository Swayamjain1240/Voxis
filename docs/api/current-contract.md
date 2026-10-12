# VOXIS — Implemented foundation contract

This document and `shared/contracts/*.schema.json` define the current wire
format. The other API documents retain historical target designs. They do not
override this implementation record. See ADR-009 for the migration decision.

## REST

All REST success responses (including health) use:

```json
{"success":true,"data":{},"meta":{"request_id":"32-character server-generated hex ID","api_version":"v1","schema_version":"1.0.0"}}
```

Errors use `success:false`, `error:{code,message,details}`, and the same metadata.
An input-compatible `detail` error field is retained temporarily. Validation
responses omit submitted values. `X-Request-ID` matches the response metadata;
the server does not trust an arbitrary incoming identifier.

| Endpoint | Input / behavior |
| --- | --- |
| `GET /` | Service identity, not translation readiness |
| `GET /api/v1/health`, `/health/live`, `/health/ready` | Component state, liveness, API-only readiness; translation remains unavailable |
| `GET /api/v1/speech/capabilities` | Actual service availability, not just enabled configuration |
| `POST /api/v1/speech/upload` | Multipart `audio`; bounded validation, no transcription/persistence |
| `POST /api/v1/speech/transcribe` | Same upload boundary; 501 disabled / 503 unimplemented |
| `GET /api/v1/sign/status` | Model availability |
| `POST /api/v1/sign/predict` | 60 x 300 finite raw features, optional `top_k` 1–10/context; 501 / 503 after validation |
| `POST /api/v1/conversation/message` | Validated user message, optional context; returns normalized message, no shared storage |
| `POST /api/v1/conversation/text-to-gloss` | JSON `{text,context?,language:"en"}`; deterministic keyword fallback |
| `POST /api/v1/conversation/gloss-to-text` | JSON `{glosses,context?,language:"en"}`; deterministic template fallback |
| `GET /api/v1/rooms/status` | Disabled |
| `POST /api/v1/rooms`, `/rooms/join` | 501; Mode 2 is not enabled |

Conversation inputs accept `id` as an alias for `message_id` and milliseconds
as a legacy timestamp. Responses always use canonical names and UTC ISO-8601.
The old text-to-gloss query input and bare-list gloss body remain compatibility
inputs; new clients send JSON, which avoids transcript text in URLs. Do not
supply both query and JSON text. IDs are 1–128 safe identifier characters; text
is 1–4000 characters; gloss arrays are at most 60 known values. Unknown fields,
sources, contexts, versions and disallowed context glosses are rejected.

`frontend/src/services/api.js` unwraps the envelope so its callers receive data,
uses a 15-second timeout, omits credentials and does not automatically retry
requests. Transcript rendering uses React text escaping and canonical IDs.

The current language conversion is a restricted keyword/template fallback,
not an ISL grammar engine or an LLM. The original text/gloss input is preserved.
No TTS route or real provider is introduced by this contract migration.

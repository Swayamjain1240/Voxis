# VOXIS — Security, architecture, and delivery register

## Purpose and scope

This record keeps the original security and architecture requirement numbering
visible while separating foundation evidence from future product work. It covers
the current local, one-device **Mode 1** foundation: browser camera/microphone
boundaries, the FastAPI service boundary, shared contracts, the restricted
vocabulary, and repository hygiene. Accounts, persistence, Mode 2, external
providers, trained models, and production operations remain deferred until their
own design and review gates.

The register deliberately preserves the original ranges **1–19, 20–25,
26–40, 41–51, and 52–60**. Some source requirements are grouped under a range;
they are not renumbered into a replacement checklist.

### Evidence states

- **Implemented (source + checked):** source behavior has a focused test or a
  recorded audit result in this checkout.
- **Implemented (source):** the narrow boundary exists, but broader integration
  or deployment evidence is still missing.
- **Partial:** a useful boundary exists, but important coverage or product flow
  is incomplete.
- **Planned / deferred:** intentionally future work or outside the current Mode
  1 foundation; it must not be presented as available.

The current verified checks are recorded in `docs/part-1.md` and the current
REST wire behavior in `docs/api/current-contract.md`. The frontend build has
completed locally, but no browser E2E, responsive viewport review, production
deployment, penetration test, or remotely executed CI run is claimed by this
document.

## Assets and trust boundaries

### Assets

- Camera frames, derived landmarks, and model inputs.
- Microphone audio, temporary upload bytes, and future transcripts.
- Glosses, confidence values, captions, conversation content, and avatar state.
- Provider credentials and configuration when optional services are enabled.
- Model files, vocabulary/label versions, dataset manifests, and license or
  consent records.
- Source history, generated files, local environments, and runtime availability.

### Trust boundaries

1. **Browser:** permission-controlled camera/microphone capture and local UI
   state; browser input is untrusted when sent to the API.
2. **Backend:** FastAPI REST parsing, validation, upload handling, and service
   boundaries; requests, headers, media, and forwarded claims are untrusted.
3. **Provider:** future Whisper, LLM, TTS, or other external service; no
   retention or training policy is assumed without a provider review.
4. **Repository/developer machine:** source, environment variables, datasets,
   model artifacts, caches, and generated files.
5. **Future remote boundary:** accounts, rooms, and two-device exchange; the
   WebSocket route is disabled and cannot be treated as a remote transport.

## Threat summary

| Threat | Current treatment | Remaining boundary |
| --- | --- | --- |
| Malformed requests exhaust the backend | Typed contracts, 1 MiB general-body limit, bounded multipart limit, per-peer quota, eight-request concurrency cap, and request deadline | Production proxy limits and workload-specific model queues are future work |
| MIME-only or oversized media reaches a service | Allowlisted audio types, container signatures, bounded chunk reads, empty/content mismatch rejection | A full codec parser/virus scanner is not part of the lightweight local foundation |
| One client receives another client’s data | `/ws` closes before acceptance; old global broadcast helpers are removed; Mode 1 uses REST | Authenticated isolated Mode 2 requires a new review |
| Credentials or private input leak through responses/logs | Safe envelopes, redacted validation details, no URL/payload/IP logging, credentials omitted by frontend, and a common-pattern scan of current/reachable history | Broader entropy/artifact scanning and provider review remain required |
| Browser origin/host spoofing reaches the API | Exact `CORS_ORIGINS`, explicit `ALLOWED_HOSTS`, no credentials, production HTTPS requirement | TLS/proxy trust configuration must be reviewed before deployment |
| Unsupported model output is presented as fact | Restricted vocabulary, explicit unavailable-service errors, `UNKNOWN` contract support | Live model confidence/rejection and complete UI fallback are future work |
| Persistent data or account compromise | No database, accounts, rooms, or durable conversation history exist in Mode 1 | Design privacy, identity, ownership, encryption, backups, and deletion before adding them |

## Original requirement register

### Controls 1–19 — foundational security and repository hygiene

| Original numbering | Original controls retained | Status | Evidence and next step |
| --- | --- | --- | --- |
| 1–19 | Secrets; environment validation; private-route/auth/server-access architecture; input validation; XSS prevention; rate limits; secure API errors; strict CORS; security headers; production debug off; audit before dependency upgrades; unused-package cleanup; private-file checks; secure DB configuration; eventual Argon2/bcrypt; Git tree/history secret scan; finishing security audit | **Partial** | Environment values are strictly parsed; typed inputs, React text rendering, bounded quotas/timeouts, safe envelopes, exact origins/hosts, response headers, production debug/TLS/OpenAPI protections, dependency audit pins, deny-by-default private-route dependencies, tracked bytecode removal, private-file checks, and no-login scope are implemented and tested. A 23-commit common-pattern history scan is clean. Database/password controls, broader artifact/entropy scanning, unused-package evidence, and final release audit remain. |

### Controls 20–25 — delivery and product-quality discipline

| Original numbering | Original controls retained | Status | Evidence and next step |
| --- | --- | --- | --- |
| 20 | Coherent test, diff, commit, and push checkpoints | **Implemented (source + checked)** | Each completed foundation checkpoint was tested, diff-checked, committed, and pushed to `Swayam`; latest verified remote commit is `0da8a7c`. |
| 21 | Continuous security | **Implemented (source)** | `.github/workflows/ci.yml` runs tests, dependency audits, tracked-file hygiene, and a reachable-history common-pattern scan; production monitoring/release review remain future work. |
| 22 | External API disclosure | **Implemented (source/docs)** | No AI/provider API was introduced; prior development dependency disclosures are recorded in the task evidence. Re-disclose before any provider is added. |
| 23 | Test every feature | **Partial** | Backend contract/security tests and frontend adapter tests exist; camera, browser capture, responsive screens, and future models still need their own tests. |
| 24 | Synchronized documentation | **Partial** | Current contract, Part 1 progress, ADRs, README, and this register are being synchronized; historical target docs still require a final wording sweep. |
| 25 | One-viewport authenticated screens | **Deferred / not applicable** | No authenticated screens exist in the no-login Mode 1 foundation. When screens are built, use routes/wizards/pagination rather than hidden overflow and verify desktop/tablet/mobile. |

### Controls 26–40 — application, API, and applicable security standards

| Original numbering | Original controls retained | Status | Evidence and next step |
| --- | --- | --- | --- |
| 26–40 | OWASP Top 10; API Top 10; applicable ASVS; threat model; RBAC/resource authorization; secure sessions; CSRF; injection prevention; SSRF; secure uploads; encryption/HTTPS; privacy/retention/deletion; audit logging; API abuse limits/timeouts; third-party API validation/webhooks; supply-chain security; admin least privilege | **Partial / deferred by boundary** | This record is the threat model; typed contracts, exact transport policy, safe errors, bounded/signature-checked uploads, HTTPS production checks, deny-by-default principal/permission/ownership dependencies, dependency audit pins, and metadata-only request logs cover the active local surface. Sessions, CSRF, SSRF/provider webhooks, encryption at rest, retention/deletion, RBAC/admin roles, and full OWASP/ASVS review require the future account/provider/database/deployment surfaces. |

### Controls 41–51 — architecture and maintainability

| Original numbering | Original controls retained | Status | Evidence and next step |
| --- | --- | --- | --- |
| 41–51 | Architecture first; modularity; separation of concerns; database design; transactions/consistency; standard APIs; resource optimization; idempotency/retries; clean code/SOLID; ADRs; backward-compatible refactoring | **Partial** | Monorepo boundaries, shared contracts, versioned REST, ADRs, deterministic vocabulary services, modular transport/configuration, bounded resource use, and compatibility aliases are present. Database/transactions/idempotency for durable work, full static quality checks, and deployment-scale resource testing are future work. |

### Controls 52–60 — verification, operations, accessibility, and safe AI

| Original numbering | Original controls retained | Status | Evidence and next step |
| --- | --- | --- | --- |
| 52–60 | Automated tests; CI/CD lint/type/security/build/test gates; performance; responsive accessibility; observability; secure deployment/rollback; backups/recovery; AI guardrails/cost controls; safe operations | **Partial / deferred** | Backend and frontend automated tests, dependency audits, request IDs, safe structured logs, feature gates, and explicit unavailable states exist. CI now defines test/build/audit/hygiene gates, but has not run in this checkout; lint/type checks, browser accessibility/responsive verification, performance baselines, deployment rollback, backups/recovery, provider cost/retention guardrails, and operational incident controls remain before production or external AI use. |

## Current Mode 1 acceptance boundary

The current foundation may demonstrate local microphone capture, a procedural
avatar, deterministic restricted-vocabulary conversion, and safe REST/service
boundaries. It is not the completed translator. The sign-side foundation still
needs:

```text
camera permission
  → live browser MediaPipe processing
  → canonical hand/pose landmarks
  → bounded frame buffer
  → visible failure states
```

Whisper, a trained sign model, LLM translation, TTS, real sign-animation clips,
accounts, a database, administrator controls, backups, and production
hardening are not claimed as available by this Part 1 checkpoint.

## Review triggers

Revisit this register before enabling:

- a third-party speech, LLM, TTS, analytics, or hosted model provider;
- raw-media persistence or conversation history;
- a trained/hosted sign model or downloadable model artifact;
- Mode 2 rooms or any remote WebSocket exchange;
- user accounts, an administrator surface, or a database; or
- production/public deployment.

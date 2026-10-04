# SilentSign — Dataset Licenses and Usage Policy

## 1. Purpose

This file is the legal/provenance checklist for every dataset used by SilentSign.

**Rule:** a dataset is not production-approved merely because it is technically usable.

Before redistribution, publishing derived assets, or commercial deployment, its license and upstream terms must be verified.

---

## 2. License Status Table

| Dataset | Current known status | SilentSign action |
|---|---|---|
| AI4Bharat INCLUDE | Dataset card previously identified as CC BY 4.0 | Keep attribution; preserve source/license record |
| ISL500 / ISL-DATA | Research/academic-use restrictions were previously reported; exact current terms must be verified before redistribution/commercial use | Treat as restricted until verified |
| `vidit031/isl-isolated-40words` | Mixed upstream provenance; no single license should be assumed for every clip | Track provenance/license per clip |
| Emergency ISL Gesture Dataset / VOXIS | License not established by the current audit report | Do not redistribute until license is verified |
| Custom SilentSign recordings | Controlled by consent/release terms created by the team | Obtain explicit participant consent |

---

## 3. AI4Bharat INCLUDE

### Current project understanding

The INCLUDE dataset card was previously identified as:

```text
CC BY 4.0
```

### Implications

Generally, CC BY 4.0 requires attribution when material is reused.

SilentSign should preserve:

```text
Dataset name
Original authors/organization
Original source link
License name
Any required attribution notice
```

### Project rule

Before final release, verify the current official dataset page and store the exact license URL/text reference in this document.

---

## 4. ISL500 / ISL-DATA

### Current status

The team previously encountered information indicating that ISL500 is intended for research/academic use and that commercial use may require author permission.

Because this has **not yet been re-verified from an authoritative current license file**, SilentSign must treat ISL500 as:

```text
RESEARCH-ONLY / RESTRICTED UNTIL VERIFIED
```

### Allowed project behavior for now

- local research
- experimentation
- model prototyping
- hackathon evaluation, subject to the actual dataset terms

### Do not assume permission for

- republishing the raw dataset
- uploading raw videos to the SilentSign repository
- commercial redistribution
- bundling source clips into a public product

### Required before release

Verify:
- repository LICENSE
- dataset card
- original paper/site
- author usage terms
- redistribution rights
- derivative-work rights

---

## 5. `vidit031/isl-isolated-40words`

### Critical provenance rule

This dataset is a wrapper/collection containing clips from multiple upstream sources.

Observed upstream provenance includes:

```text
ISL500
INCLUDE
CISLR
ISLRTC dictionary
```

Therefore:

```text
wrapper dataset license ≠ automatically the license of every clip
```

### Required manifest fields

Every selected clip should record:

```text
clip_id
sign
wrapper_dataset
upstream_source
source_url
license
review_status
redistribution_allowed
```

### Current project policy

Only use clips whose source and terms are sufficiently understood.

If provenance is unclear:

```text
training candidate → HOLD
redistribution → NO
avatar publication → NO
```

until verified.

---

## 6. Emergency ISL Gesture Dataset / VOXIS

### Current status

Rishi's technical audit established:
- signs
- participant counts
- raw/cropped video counts
- video integrity

It did **not** establish a license.

Therefore current license state is:

```text
UNKNOWN / NOT YET VERIFIED
```

### Policy

The team may keep the local copy for audit/testing while its legitimate source and license are being checked.

Do not:
- upload the raw videos to GitHub
- send the full dataset publicly
- bundle videos into the final app
- publish derived avatar assets if the license forbids derivatives

until terms are confirmed.

---

## 7. Raw vs Derived Data

License review must consider both:

### Raw data

```text
videos
images
audio
metadata
```

### Derived data

```text
MediaPipe landmarks
normalized arrays
trained model weights
avatar motion clips
animations
```

A license may allow research on raw data while restricting redistribution of derived assets.

Do not assume that "derived" automatically means unrestricted.

---

## 8. Custom SilentSign Recordings

If the team records its own sign samples, create a simple contributor/participant consent process.

At minimum record:

```text
participant_id
date
purpose
permission to use for training
permission to use for demo
permission to publish derived landmarks
permission to publish video, if applicable
```

Prefer keeping raw participant video private unless public release is specifically required.

---

## 9. Repository Rules

Never commit:

```text
raw third-party dataset archives
full third-party video collections
credentials/tokens used to download data
private participant information
```

Repository should contain:

```text
source links
dataset registry
manifest
license notes
attribution
processing scripts
```

---

## 10. Pre-Release License Checklist

Before hackathon submission/public release:

- [ ] Verify official INCLUDE license
- [ ] Add INCLUDE attribution
- [ ] Verify current ISL500 usage terms
- [ ] Verify redistribution rules for selected ISL500 clips
- [ ] Resolve provenance/license for each 40-word clip actually used
- [ ] Verify VOXIS/emergency-dataset license
- [ ] Check whether derived landmark files may be shared
- [ ] Check whether avatar motion derived from dataset clips may be published
- [ ] Store license/source references in `dataset_registry.csv`
- [ ] Remove any unlicensed raw asset from the repository/build
- [ ] Confirm custom-recording consent if custom data is added

---

## 11. Engineering Rule

A dataset has three independent states:

```text
TECHNICALLY VALID
LICENSE VERIFIED
REDISTRIBUTION APPROVED
```

Do not collapse these into one status.

Example:

```text
PAIN / ISL500
Technically valid: YES
License verified: PENDING
Redistribution approved: PENDING
```

This distinction must remain visible throughout the project.

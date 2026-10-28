# CDX-WP07 — Final Acceptance & Release Decision

**Status:** PREFLIGHT COMPLETE — RELEASE BLOCKED BY EXTERNAL GATES  
**Target:** CDX 1.0.0  
**Candidate:** `CDX-DIST-1.0.0-RC1`  
**Date:** 2026-10-28

## 1. Preflight result

The CDX 1.0 core is internally closed enough to make the final release decision mechanically well-defined.

The preflight result is nevertheless:

`BLOCKED_EXTERNAL_GATES`

This is not a failure of the CDX architecture. After WP04 verification, the release remains correctly fail-closed because one release-critical control — native/equivalent repository protection — is still not independently proven.

## 2. Internal conditions now satisfied

- constitutional Act: `ADOPTED v1.0.0`;
- RC-01 boundary: frozen, no exception;
- reference runtime: verified;
- `CDX-RUNTIME-001 v1.0.0`: frozen release candidate;
- 69 machine controls: self-test PASS;
- review-governed constitutional surface: previously accepted;
- SPETL v1.1: canonical + portable compatibility PASS;
- candidate distribution: `CDX-DIST-1.0.0-RC1`;
- candidate artifacts: pinned by Git blob SHA and reproducibly verifiable;
- canonical consumer binding contract: `.cdx/anchor.json`.

## 3. Core blockers

### #5 — Native repository protection

State: `PLATFORM_PLAN_GATE_BLOCKED`.

GitHub reports that rulesets for this private repository require an upgraded capability or public visibility. Current integration cannot administer protection. Existing in-repo controls are post-push and therefore not an equivalent pre-merge guarantee.

### #17 — Independent SPETL evidence custody

State: **CLOSED / VERIFIED REFERENCE CUSTODY**.

`CDX-CUSTODY-GHA-001` was verified through an observed main-branch producer → separate custodian → separate verifier chain with immutable artifact digests, custody receipt, re-read verification and the required negative matrix. The long-lived Vercel target remains an optional stronger retention target and is still externally provisioning-blocked, but it is no longer a core-release evidence blocker.

## 4. Release order

WP07 creates `CDX-RELEASE-1.0.0` in state:

`PENDING_BLOCKER_CLOSURE`

No human release decision is requested yet. The decision becomes legitimately requestable only after the remaining repository-protection blocker closes and all final gates pass.

## 5. Repository metadata hygiene

Two metadata items remain outside the constitutional/runtime blockers:

1. Issue #14: repository description still says “Conduct of Excellence”; canonical derivation is “Code of Conduct + Excellence”.
2. Repository homepage currently points to `https://udl-twin.vercel.app`.

The current connector cannot update repository metadata. The homepage is surfaced for owner review rather than changed by assumption.

## 6. Actions prohibited while blocked

CDX must not:

- create/publish the `1.0.0` release tag;
- set `release_state=RELEASED`;
- set `enforcement_state=ENFORCEMENT_READY` or `ENFORCING`;
- begin WP08 estate rollout as if the core release were complete;
- redefine the remaining external blocker to make the preflight pass.

## 7. Resume path

After owner-side platform actions:

1. complete WP05 native/equivalent repository-protection verification;
2. merge the repository-protection closure evidence;
3. rerun WP07 preflight;
4. if PASS, request explicit human-sovereign decision on `CDX-RELEASE-1.0.0`;
5. only after that decision and final protected PR: publish CDX 1.0.0 and proceed to WP08.

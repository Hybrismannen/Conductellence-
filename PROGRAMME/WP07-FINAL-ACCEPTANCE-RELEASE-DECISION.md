# CDX-WP07 — Final Acceptance & Release Decision

**Status:** RELEASE DECISION RECORDED — PUBLICATION READY, EXPLICIT AUTHORIZATION PENDING  
**Target:** CDX 1.0.0  
**Candidate:** `CDX-DIST-1.0.0-RC1`  
**Date:** 2026-10-29

## 1. Final acceptance state

WP07 has completed the release-decision stage.

Canonical state:

- constitutional state: `ADOPTED`;
- core runtime: `VERIFIED_REFERENCE_RUNTIME`;
- core release blockers: none;
- WP04 independent evidence custody: VERIFIED;
- WP05 native repository protection: VERIFIED;
- WP06 runtime/distribution closure: complete;
- sovereign release decision: `RELEASE_1_0_0`;
- repository release state: `PRE_RELEASE`;
- enforcement state: `BOOTSTRAP`.

The sovereign decision was recorded through PR #45 and canonicalized through PR #46.

That decision is intentionally distinct from publication authority.

## 2. Publication readiness verification

Exact-head publication readiness was verified against main commit:

`c3c751733dbace3e051c628f3d68dc706427eb6f`

Evidence includes:

- Law Audit run `40869176000` — PASS;
- release preflight — PASS;
- `CDX-DIST-1.0.0-RC1` artifact blob set pinned and reproducible — PASS;
- core blocker set `[]`;
- SPETL custody verifier run `40869232554` — PASS;
- protected `main` with all five required CDX status contexts;
- frozen release boundary with no active exceptions;
- GitHub Releases collection empty at verification time.

Canonical readiness record:

`GOVERNANCE/release/CDX-1.0-PUBLICATION-READINESS-2026-10-29.json`

## 3. Remaining sovereign gate

The only remaining WP07 gate is:

`EXPLICIT_HUMAN_SOVEREIGN_AUTHORIZATION_TO_PUBLISH_CDX_1_0`

A generic proceed instruction, normal PR approval or `/cdx-approve` does not itself create publication authority.

The publication authorization must explicitly authorize publication of CDX 1.0.0.

## 4. Publication operation after authorization

After explicit publication authority:

1. create the final publication-state PR;
2. bind the release to that exact protected merge commit;
3. pass all required CDX checks;
4. receive exact-head `/cdx-approve`;
5. merge the publication-state transition;
6. verify the target tag does not already exist;
7. create tag `1.0.0`;
8. publish GitHub Release `CDX 1.0.0`;
9. re-read tag/release provenance;
10. reconcile canonical state to `RELEASED`.

Publication does not imply estate-wide enforcement or runtime binding.

## 5. Post-release boundary

Only after CDX 1.0.0 publication and post-publication verification may WP08–WP14 proceed as release-dependent estate work.

The estate enforcement blocker remains a separate axis.

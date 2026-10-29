# CDX 1.0 — Publication gate review (PUBLISHED AND VERIFIED)

**Date:** 2026-10-29  
**Sovereign release decision:** `RELEASE_1_0_0`  
**Publication authorization:** GRANTED and EXECUTED  
**Tag:** `1.0.0`  
**Publication commit:** `6e275dea737d77349ddd1264c4f6ef900904995f`  
**GitHub Release:** `427882220` — CDX 1.0.0  
**Canonical release state after reconciliation:** `RELEASED`  
**Enforcement state:** `BOOTSTRAP`

## Verified publication chain

1. Core release blocker set was empty.
2. Native protected-main controls remained verified.
3. Independent SPETL reference custody remained verified.
4. `CDX-DIST-1.0.0-RC1` artifact blob set verified as pinned and reproducible.
5. Explicit human-sovereign release decision `RELEASE_1_0_0` was recorded.
6. Separate explicit publication instruction `I authorize publication of CDX 1.0.0.` was recorded.
7. Publication workflow run `40879564779` re-ran release preflight and package verification.
8. The workflow confirmed tag/release absence before publication.
9. Annotated tag `1.0.0` was created and resolves to commit `6e275dea737d77349ddd1264c4f6ef900904995f`.
10. GitHub Release `CDX 1.0.0` was published and independently re-read.
11. Publication provenance and the RC manifest were uploaded as release assets.

Canonical evidence:

`GOVERNANCE/release/CDX-1.0-PUBLICATION-EVIDENCE-2026-10-29.json`

## Separation of states

Publication closes the CDX 1.0 **core release**.

It does not establish:

- estate-wide `ENFORCING`;
- downstream `VERIFIED_RUNTIME_BOUND`;
- FFOS runtime activation;
- Pius binding verification;
- FFC admission;
- estate-wide propagation.

The governing rule remains:

**Maturity is not enforcement. Release is not integration. Integration is not estate-wide enforcement.**

## Tag-signature note

The annotated Git tag is unsigned. Signed tags were not a CDX 1.0 release criterion. The tag object SHA, target commit, publication workflow, Release ID and release-asset digests are preserved as publication evidence.

**Gate result:** `PASS / PUBLISHED_VERIFIED`.

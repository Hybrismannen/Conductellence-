# CDX-WP07 — Final Acceptance & Release Decision

**Status:** COMPLETE — CDX 1.0.0 PUBLISHED AND VERIFIED  
**Release:** `1.0.0`  
**Publication commit:** `6e275dea737d77349ddd1264c4f6ef900904995f`  
**GitHub Release:** `CDX 1.0.0` / ID `427882220`  
**Date:** 2026-10-29

## 1. WP07 result

WP07 is complete.

CDX 1.0.0 has passed the full governed release chain:

```text
zero core blockers
→ explicit RELEASE_1_0_0 decision
→ publication readiness verification
→ separate explicit publication authorization
→ protected publication PR
→ exact-commit release preflight
→ pinned package verification
→ tag 1.0.0
→ GitHub Release CDX 1.0.0
→ independent publication re-read
→ canonical RELEASED reconciliation
```

## 2. Published release evidence

- tag: `1.0.0`;
- annotated tag object: `c0233574e7fb850cb3e358f869c31cb38fe822b9`;
- tag target commit: `6e275dea737d77349ddd1264c4f6ef900904995f`;
- publication workflow run: `40879564779`;
- GitHub Release ID: `427882220`;
- publication time: `2026-10-29T13:10:59Z`;
- provenance asset digest: `sha256:a3ac18df7e436a4ec62271a0d64aeaf570152c773f19316c45a8889666b8506d`;
- RC manifest release-asset digest: `sha256:f4504dcca9c21b460868c65c1a9aed55cec8a909f5db101588fee57349831ac1`.

Canonical evidence:

`GOVERNANCE/release/CDX-1.0-PUBLICATION-EVIDENCE-2026-10-29.json`

## 3. Canonical state after WP07

- constitutional: `ADOPTED`;
- core runtime: `VERIFIED_REFERENCE_RUNTIME`;
- release: `RELEASED`;
- enforcement: `BOOTSTRAP`;
- estate integration: `PENDING_RUNTIME_BINDINGS`;
- core release blockers: none;
- estate enforcement blocker: `CDX-BLOCK-ESTATE-RUNTIME-001`.

## 4. What WP07 does not complete

CDX 1.0 publication does not automatically complete downstream governance.

The release boundary explicitly places the following work outside the 1.0 core closure:

- WP08 — Estate Registry v2 applicability classification;
- WP09 — canonical anchor migration;
- WP10 — estate anchor verification and reconciliation;
- WP11 — FFOS first verified runtime binding;
- WP12 — Pius binding verification;
- WP13 — FFC admission;
- WP14 — estate-wide CDX 1.0 propagation.

Those are separate release-dependent work packages and may now begin.

## 5. State discipline

The governing maxim remains:

**Maturity is not enforcement. Release is not integration. Integration is not estate-wide enforcement.**

# CDX-WP02 — RC-01 Core Boundary Freeze

**Status:** EXECUTED FOR REVIEW  
**Boundary:** `CDX-RC-01`  
**Target release:** `1.0.0`  
**Baseline main:** `ada82874fd0a018241a0b7b77fa0b796a63483a1`  
**Date:** 2026-10-28

## 1. Decision

CDX now has enough architecture to enter a **closure regime**.

WP02 therefore freezes the **capability boundary** for CDX 1.0. The freeze does not freeze text, bugs or implementation quality. It prevents the system from expanding sideways while the remaining 1.0 prerequisites are being closed.

The governing distinction is:

```text
BOUNDARY FROZEN
≠
CONTENT IMMUTABLE
≠
RELEASED
≠
ENFORCING
```

CDX remains `FOUNDATIONAL_DRAFT / VERIFIED_REFERENCE_RUNTIME / PRE_RELEASE / BOOTSTRAP / PENDING_RUNTIME_BINDINGS`.

## 2. What RC-01 freezes

RC-01 freezes five structural dimensions:

1. **Top-level capability domains.** The existing CDX architecture is the 1.0 architecture. No new top-level capability engine may be introduced before release closure.
2. **Constitutional surface.** `CDX-LAW-001` remains the governing law and its current 131 section IDs define the 1.0 normative surface.
3. **Auditability grammar.** The five current auditability classes are frozen.
4. **Enforcement-surface grammar.** The 18 current policy enforcement-surface classes are frozen.
5. **Human/review governance grammar.** The four canonical review procedure classes are frozen.

The machine-readable source is `GOVERNANCE/release-candidate-boundary.json`.

## 3. What may still change

Closure work is explicitly permitted inside the frozen boundary:

- defect repair;
- blocker closure;
- assurance hardening;
- constitutional adoption or clarification without silently adding new section IDs;
- legal-reference correction;
- release engineering;
- distribution-contract hardening;
- documentation and state reconciliation.

This means WP03+ can still make substantive corrections. The rule is that they must **finish what CDX already is**, not invent a new CDX while trying to release it.

## 4. What may not change silently

Before 1.0, the following require a new Director-approved boundary decision (`RC-02+`):

- a new top-level capability domain;
- a new law section ID;
- a new auditability class;
- a new enforcement-surface class;
- a new review-authority class;
- a new autonomous authority source;
- any feature expansion presented as if it were merely blocker closure.

This is an anti-expansion gate, not an anti-improvement gate.

## 5. Frozen 1.0 architecture

### Constitutional and epistemic authority
- `LAW`
- `INTERPRETATION`
- `appendices`
- `GLOBAL-AUTHORITY-CORPUS`
- `LEGAL-REFERENCES`
- `LEGAL-RESOLVER`
- `REGULATORY-DRIFT`
- `EVIDENCE-AUTHORITY`

### Operational governance
- `CONTROL-CATALOGUE`
- `REVIEW-CATALOGUE`
- `POLICY`
- `SPETL`
- `SECURITY-TWIN`
- `RED-TEAM`
- `AUDITS`

### Distribution and integration contracts
- `DISTRIBUTION`
- `RUNTIME-INTEGRATION`
- `ESTATE-REGISTRY`

### Governance and programme support
- `GOVERNANCE`
- `.github`
- `PROGRAMME`
- reserved future release-packaging root: `RELEASE`

`RELEASE` is reserved as release engineering support and is **not** a new capability domain.

## 6. Core 1.0 closure versus estate rollout

WP02 makes the release boundary explicit.

### Must close for CDX core 1.0

Two existing core blockers remain mandatory:

- `CDX-BLOCK-REPO-PROTECTION-001` — constitutional amendment path must have verified native/equivalent protection.
- `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001` — SPETL evidence must have independently verifiable preservation in a separate trust domain.

Release engineering must also produce an immutable/versioned 1.0 package and acceptance record, and repository metadata naming drift (#14) must be corrected as release hygiene.

### Not required to publish the CDX core 1.0 release

The following are **estate rollout/enforcement work**, not reasons to keep expanding the core architecture:

- `CDX-BLOCK-ESTATE-RUNTIME-001` — estate-wide consequential runtime verification;
- `CDX-ANCHOR-ESTATE-001` — full downstream anchor migration;
- WP08 full Registry v2 / applicability classification.

Those remain necessary for later estate-wide `ENFORCING`, but they do not redefine what the CDX 1.0 core is.

## 7. Enforcement

WP02 introduces `AUD-CDX-RC-BOUNDARY-001`.

The audit checks that:
- RC-01 exists and remains `FROZEN_FOR_CLOSURE`;
- all frozen top-level domains remain present;
- unreserved new top-level domains are rejected;
- the 131 frozen section IDs remain exact;
- auditability, enforcement-surface and review-procedure grammars remain exact;
- default policy behavior remains `DENY_ON_CONTROL_ERROR`;
- the current CDX state has not been promoted merely because the boundary is frozen.

The audit runs on pull requests and pushes to `main`.

## 8. Amendment path

A legitimate reason may emerge to change the boundary before 1.0. That is allowed only through an explicit boundary amendment:

```text
Director decision
→ reason and impact recorded
→ new boundary candidate RC-02+
→ protected PR
→ full CDX audits
→ human merge
```

RC-01 itself must not simply be edited to pretend the expansion was always inside scope.

## 9. Handoff

WP02 closes when the RC-01 boundary audit passes on the WP02 PR and the package is merged.

Next work package:

**CDX-WP03 — Constitutional Adoption & 1.0 Normative Freeze**

WP03 resolves whether and how the current `FOUNDATIONAL_DRAFT` law becomes the adopted 1.0 constitutional source without expanding the RC-01 boundary.

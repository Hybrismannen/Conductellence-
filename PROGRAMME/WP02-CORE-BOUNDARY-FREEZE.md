# CDX-WP02 — RC-01 Core Boundary Freeze

Status: EXECUTED FOR REVIEW  
Date: 2026-10-28  
Boundary ID: `CDX-RC01-BOUNDARY-001`  
Target release: **CDX 1.0**

## 1. Decision

The Conductellence 1.0 core boundary is frozen.

WP03–WP07 are closure work. They may repair, harden, verify and release the existing CDX architecture, but they may not enlarge the constitutional/product architecture merely because additional ideas become available during closure.

The governing maxim for RC-01 is:

> **CDX 1.0 is completed by satisfying existing obligations, not by adding new ones.**

## 2. What is frozen

The following identities remain canonical through the 1.0 closure sequence:

- system: `CDX-SYS-001`
- law: `CDX-LAW-001`
- runtime contract: `CDX-RUNTIME-001`
- estate anchor standard: `CDX-GOV-ANCHOR-001`
- scientific evidence authority: `CDX-EVID-001`
- short name: `CDX`
- name derivation: **Code of Conduct + Excellence**

The constitutional topology is also frozen for closure:

- **7 Foundational Principles**
- **131 law sections**
- **69 FULLY_AUTOMATABLE sections**
- **62 review-governed sections**

Changing these counts is treated as a boundary change, not ordinary closure work.

## 3. Frozen core domains

The 1.0 core consists of the existing law-first stack and its supporting assurance/release surfaces:

`LAW → INTERPRETATION → CONTROL-CATALOGUE → POLICY → AUDITS → SPETL → SECURITY-TWIN → APPENDICES`

with the already-established supporting domains:

- Global Authority Corpus
- legal references and Legal Resolver
- regulatory drift
- scientific Evidence Authority
- review governance
- red-team/adversarial acceptance
- Distribution
- Runtime Integration
- Governance
- Estate Registry
- programme and CI surfaces needed to evidence closure.

A new first-class CDX subsystem is **not** closure work.

## 4. Allowed closure changes

WP03–WP07 may:

- correct defects and contradictions;
- strengthen controls, tests, schemas and evidence;
- implement the independent SPETL custody already required by blocker #17;
- establish the repository/release protection already required by blocker #5;
- finalize existing distribution and runtime contracts;
- make state transitions already present in the state model after their gates pass;
- produce release artifacts and migration instructions;
- update audits and programme evidence.

This allows substantive engineering while preventing architectural drift.

## 5. Changes prohibited without an explicit boundary exception

The following may not enter CDX 1.0 silently:

- new top-level first-class CDX subsystem/domain;
- new or removed Foundational Principle;
- new or removed `CDX-LAW-001` section;
- replacement of canonical identities;
- parallel short name to `CDX`;
- non-human sovereignty or authority above human sovereign authority;
- universal-super-admin semantics;
- collapsing binding/runtime/release/enforcement states into a single status;
- “closing” a blocker by redefining away its requirement;
- downstream product/business logic imported into the CDX core.

## 6. Boundary exception

A genuine scope change remains possible, but it must be explicit.

An approved exception must be recorded under:

`GOVERNANCE/orders/CDX-BOUNDARY-EXCEPTION-*.json`

and must identify the requested change, reason, affected frozen element and human decision.

There are **no active boundary exceptions** at WP02 closure.

## 7. Estate work is deliberately deferred

The accepted 31-repository topology remains binding programme intent, but full execution is not part of the CDX 1.0 **core closure**.

The following remain downstream programme WPs:

- WP08 — Registry v2 / 31-repository applicability classification
- WP09 — canonical anchor migration
- WP10 — anchor verification
- WP11 — FFOS runtime binding
- WP12 — Pius verification
- WP13 — FFC admission
- WP14 — estate-wide propagation

This distinction is important: CDX 1.0 must become a stable authority **before** it is propagated across the estate.

## 8. Automated guard

WP02 adds `AUDITS/audit_release_boundary.py`.

The audit verifies:

- boundary state and canonical IDs;
- the 7/131/69/62 frozen topology;
- required closure WPs and deferred estate WPs;
- absence of unapproved boundary exceptions in the boundary record;
- no unexpected new top-level first-class directory.

The audit is wired into both the Law Audit and Remediation Readiness workflows.

The Constitutional Mutation Guard is also broadened to treat all frozen core governance/release surfaces as protected for the existing PR-only tripwire. This does **not** solve the native repository-protection blocker; it only aligns the in-repo degraded control with the frozen release boundary.

## 9. State effect

WP02 does **not** change:

- constitutional state: `FOUNDATIONAL_DRAFT`
- core runtime: `VERIFIED_REFERENCE_RUNTIME`
- release: `PRE_RELEASE`
- enforcement: `BOOTSTRAP`
- estate integration: `PENDING_RUNTIME_BINDINGS`

It adds a separate release-boundary state:

`FROZEN_FOR_CLOSURE`

## 10. Handoff

WP02 completion authorizes **WP03 — RC-02 Constitutional Closure** to work only inside the frozen boundary.

If WP03 discovers that the Act genuinely requires structural expansion rather than correction/adoption, it must stop that change and create a boundary exception rather than silently modifying the baseline.

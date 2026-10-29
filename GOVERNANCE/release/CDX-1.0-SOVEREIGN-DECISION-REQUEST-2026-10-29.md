# CDX 1.0 — Sovereign Release Decision Record (UNDECIDED)

**Order:** `CDX-RELEASE-1.0.0`  
**Candidate:** `CDX-DIST-1.0.0-RC1`  
**Decision state:** `AWAITING_EXPLICIT_HUMAN_SOVEREIGN_DECISION`  
**Release authorized:** `false`  
**Prepared:** 2026-10-29

## Decision context

WP05 repository-protection closure and WP07 final preflight dossier are present on canonical `main`. Current `GOVERNANCE/orders/CDX-RELEASE-1.0.0.json` is `READY_FOR_DECISION` with `decision=null`, and `GOVERNANCE/system-state.json` is `PRE_RELEASE` with zero core release blockers. The independent reference custody and release candidate pinning are recorded in the canonical repository.

This record is a **decision-request template only**, not a decision. A normal `/cdx-approve` GitHub PR comment approves a specific pull-request head; it **does not** authorize CDX 1.0 publication.

## Sole authorized sovereign choices

- `RELEASE_1_0_0` — a distinct, explicit human sovereign choice to authorize the versioned CDX 1.0 release, after final exact-head gate verification.
- `HOLD` — retain `PRE_RELEASE` and all fail-closed boundaries.
- `RETURN_FOR_REMEDIATION` — require corrective changes and fresh gates.

**Recorded choice:** NONE.  
**Decision by:** NONE.  
**Decision at:** NONE.  
**Release publication:** NOT STARTED.

## Requirements following a RELEASE_1_0_0 choice

Validate the exact final decision PR head and all required CDX GitHub checks, receipt of sovereign release authorization in the designated canonical release order, package blob verification, custody/protection consistency and release boundary before any tag or release publication. Changes to release flags, tags, integrations and downstream bindings must be a separate governed operation. Never treat approval of this documentation as permission for those side effects.

**Prohibited now:** create a CDX 1.0 tag, publish a GitHub Release, set `release_state=RELEASED`, change estate enforcement to `ENFORCING`, begin WP08 rollout, or activate FFOS F8.7.
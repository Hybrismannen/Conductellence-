# CDX WP07 — Final release-decision preflight dossier (2026-10-29)

**Decision authority:** HUMAN_SOVEREIGN_AUTHORITY (not delegated to an agent)  
**Release candidate:** `CDX-DIST-1.0.0-RC1`  
**Release order:** `CDX-RELEASE-1.0.0`  
**Current order state:** `READY_FOR_DECISION`; `decision=null`; `release_authorized=false`.  
**Disposition of this PR:** Documentation-only final gate review; NOT a release authorization or release tag.

## Verified canonical source on main

- `GOVERNANCE/system-state.json`: `core_release_blockers=[]`, `release_state=PRE_RELEASE`, `enforcement_state=BOOTSTRAP`.
- `GOVERNANCE/repository-protection-state.json`: `VERIFIED_NATIVE_PROTECTION` with enforcing requirement satisfied.
- `GOVERNANCE/repository-protection-verification.json`: `VERIFIED`, criteria accepted, referencing authenticated GitHub protection readback and observed non-draft negative gate.
- `GOVERNANCE/release-preflight-state.json`: `READY_FOR_HUMAN_RELEASE_DECISION`, `release_authorized=false`.
- `GOVERNANCE/orders/CDX-RELEASE-1.0.0.json`: `READY_FOR_DECISION`, explicit human sovereign authority, no decision yet.
- `SPETL/custody/deployment-state.json`: independent GitHub Actions reference custody `VERIFIED_REFERENCE_CUSTODY`, `satisfies_enforcing_requirement=true`. External Vercel long-lived custody target remains blocked but is not a core blocker under the accepted reference-custody rule.
- `DISTRIBUTION/releases/1.0.0-rc1/manifest.json`: seven pinned Git blob artifacts, release candidate status unchanged, no release authorization.

## Release-candidate evidence and final preflight

`AUDITS/audit_release_preflight.py` verifies the pinned release artifact with `DISTRIBUTION/build_release_package.py --verify-only`, checks adopted constitution, frozen boundary, runtime contract, custody/protection consistency, zero blockers, and undecided human decision state. The CI runs for the final PR must complete and be reviewed on its exact final head SHA. No workflow result is assumed merely because this document exists.

**Manifest nuance:** `manifest.release_gate.current_state=BLOCKED_EXTERNAL_GATES` is historical candidate-package metadata, while latest canonical `system-state` and `release-preflight-state` show zero blockers. Do not rewrite pinned manifest bits as an incidental edit: preserve immutable candidate provenance; use authoritative live governance state for a decision and record the superseded metadata explicitly.

## Gates before sovereign decision

1. All five native branch-required contexts PASS on the final decision PR head: `constitutional-audit`, `mutation-guard`, `readiness`, `state-reconciliation`, `human-sovereign-approval`.
2. Release preflight and artifact blob verification PASS on the exact reviewed commit.
3. Independent custody provenance and canonical WP05 protection evidence remain valid.
4. No new exceptions, blockers or boundary drift.
5. An explicit **separate release decision** by human sovereign authority is recorded using one of `RELEASE_1_0_0`, `HOLD` or `RETURN_FOR_REMEDIATION`. The normal PR `/cdx-approve` means approval of the PR head, **not** authorization to publish CDX 1.0.
6. After the explicit release decision, implement a separate governed authorization/publishing process with verification. No autonomous tag, deployment, FFOS binding, or `RELEASED` state change is permitted by this dossier.

## Explicit hold

This PR must not mutate `GOVERNANCE/orders/CDX-RELEASE-1.0.0.json` decision fields, `GOVERNANCE/system-state.json` release/enforcement fields, release artifact status, tag, or estate runtime bindings.

**Next human decision (only after final gates):** `RELEASE_1_0_0` / `HOLD` / `RETURN_FOR_REMEDIATION`.
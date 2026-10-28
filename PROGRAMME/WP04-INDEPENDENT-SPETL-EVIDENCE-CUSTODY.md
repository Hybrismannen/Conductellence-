# CDX-WP04 — Independent SPETL Evidence Custody

**Status:** REFERENCE CUSTODY IMPLEMENTED — OBSERVED VERIFICATION REQUIRED  
**Blocker:** `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001`  
**Custody profiles:** `CDX-CUSTODY-GHA-001` (reference) + `CDX-CUSTODY-001` (long-lived target)  
**Date:** 2026-10-28

## 1. Objective

WP04 closes the release-critical evidence-independence obligation without confusing local tamper detection with independent custody. The local SPETL hash chain remains useful, but the same runtime that emits evidence must not have unrestricted power to rewrite or erase its own history.

Target pattern:

```text
governed runtime / policy decision
        ↓ SPETL event + hash chain
trusted publication workflow
        ↓ short-lived GitHub OIDC
CDX-CUSTODY-001 (separate Vercel project)
        ↓ Vercel OIDC
private Blob evidence store
        ↓
independent read / digest / chain verification
```

## 2. Canonical event contract

SPETL event schema v1.1 now requires correlation/causation IDs, run and trace references, actor and pseudonymous subject reference, authority and mandate references, pinned policy version/digest, decision, attempted and actual effect, reviewer, control/evidence references, explicit data-minimization metadata, and hash-chain fields.

Incomplete events are rejected rather than silently downgraded.

## 3. Custody bundle

A verified event chain is packaged as `cdx.spetl.custody-bundle/v1.0` with producer identity, source commit, the complete expected event-ID set, retention disposition and SHA-256 bundle digest. The expected-ID set makes withholding detectable even if an attacker recomputes the outer digest.

## 4. Separate custody implementation

The target is a Vercel project `cdx-spetl-custody` with private Blob store `cdx-spetl-evidence`.

The runtime receives no Blob administrator credential. GitHub Actions authenticates to the gateway using short-lived OIDC. The Vercel custody project accesses its connected private Blob store through the project-to-Blob binding; the governed runtime does not receive that storage binding.

The service exposes only:
- POST `/api/v1/evidence`
- POST `/api/v1/verify`
- GET `/api/health`

There is no delete/update endpoint. Evidence pathnames include bundle identity and digest and are written with overwrite disabled.

## 5. Rights, retention and minimization

Direct personal data is prohibited by default. Subject references should be pseudonymous and each event declares its minimization posture.

Objects are preserved until governed disposition. Any legally required deletion is a separate administrative action after privacy/legal review, with authority and reason recorded and a non-content tombstone retained where lawful.

## 6. Test matrix

Local contract tests cover:
- ALLOW;
- DENY;
- policy-unavailable SECURITY_STOP;
- missing required event;
- tamper;
- withheld evidence;
- forged authority;
- different runtime identity;
- untrusted repository identity.

External verification must additionally prove a valid main-workflow OIDC write, wrong-identity denial, private-object re-read/verification and missing-object loss detection.

## 7. State discipline

This implementation PR does not close blocker #17.

Until the external Vercel project/store are provisioned and the full matrix is observed:
- independent preservation remains non-verified;
- `satisfies_enforcing_requirement=false`;
- blocker #17 remains in `core_release_blockers`;
- release remains `PRE_RELEASE`;
- enforcement remains `BOOTSTRAP`.

## 8. Closure sequence

1. Merge the custody contract/implementation after CDX CI passes.
2. Provision the separate Vercel project and private Blob store.
3. Deploy from merged `SPETL/custody-service`.
4. Bind the trusted publication workflow to the real endpoint.
5. Run the external positive/negative matrix.
6. Record project/store/deployment identifiers and receipts.
7. Only if all tests pass: set custody `VERIFIED_EXTERNAL`, set independent preservation `VERIFIED`, remove blocker #17, and rerun all release gates.


## 9. External provisioning result — BLOCKED

On 2026-10-28, provisioning of the dedicated Vercel project `cdx-spetl-custody` from merged source was attempted in team `linus-fasts-projects`.

Vercel returned HTTP 402 `resource_creation_blocked` because the team account has an overdue balance. This is an external account-control gate; Conductellence cannot and must not alter billing automatically.

The visible Vercel project inventory was reviewed. No existing project is a safe custody substitute: each is linked to an active or historically meaningful application/repository. Repurposing one to bypass billing would contaminate the separate-trust-domain requirement.

Therefore:

- custody implementation remains merged and valid;
- deployment state becomes `PROVISIONING_BLOCKED_EXTERNAL_ACCOUNT`;
- external verification remains unrun;
- `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001` remains open;
- release remains `PRE_RELEASE`;
- enforcement remains `BOOTSTRAP`.

Required external action: restore the Vercel team's billing/payment status. After that, resume at provisioning step 2 without redesigning WP04.


## 10. Executable independent reference custody — CDX-CUSTODY-GHA-001

Because long-lived Vercel provisioning is externally blocked, WP04 also defines a separately approved **reference custody** profile rather than weakening or bypassing the evidence-independence requirement.

The reference chain is:

```text
SPETL Evidence Producer
        ↓ immutable producer artifact
separate workflow_run
SPETL Independent Custodian
        ↓ custody bundle + SHA-256 receipt
separate workflow_run
SPETL Custody Verifier
        ↓ verification report
GitHub Actions artifact service
```

The producer, custodian and verifier are separate workflow runs. The custodian and verifier check out trusted `main` code, have only read permissions to repository contents/actions, and do not execute code supplied in the producer artifact. The producer has no custodian storage-administrator credential.

Integrity is layered through the SPETL event hash chain, custody-bundle SHA-256, custody-receipt SHA-256, immutable artifact digest and workflow-run provenance.

Reference artifacts use 90-day retention. Direct personal data is prohibited in this reference profile; evidence uses pseudonymous subject references and explicit data-minimization metadata. Long-lived evidence must be exported to an approved long-lived custodian before expiry when preservation beyond the reference window is required.

Human approval of both custody profiles is recorded in `GOVERNANCE/orders/CDX-EVIDENCE-CUSTODY-APPROVAL-001.json`.

## 11. Canonical event-contract hardening

The SPETL v1.1 contract now also requires:
- `request_id`;
- explicit `policy_ref` in addition to policy version/digest;
- exact event-field grammar;
- exact expected event identity/order in custody bundles.

Fail-closed semantic rules reject:
- DENY/STOP decisions reported as `PERMITTED`;
- ALLOW decisions reported as `BLOCKED`;
- policy-unavailable evidence that does not stop/deny the effect;
- duplicate, injected or withheld event identities;
- arbitrary extra top-level event payload fields.

## 12. Reference-profile verification gate

The reference profile does **not** close blocker #17 merely by merging.

Closure requires an actual main-branch observation of:
1. successful producer workflow;
2. successful separate custodian workflow;
3. custody artifact ID and platform digest;
4. successful separate verifier workflow;
5. verification artifact ID and platform digest;
6. successful re-read of the custody receipt and verification report;
7. PASS for ALLOW, DENY, policy-unavailable, denied-effect contradiction, invalid event, tamper, withheld/loss, different runtime identity, forged authority and write/read/verify provenance.

Only after those observations may the independent-preservation state become `VERIFIED` and blocker #17 be removed. The Vercel profile remains the preferred long-lived production target when external provisioning becomes available.

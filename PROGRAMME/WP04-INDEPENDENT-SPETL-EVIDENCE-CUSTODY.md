# CDX-WP04 — Independent SPETL Evidence Custody

**Status:** IMPLEMENTATION STAGED — EXTERNAL PROVISIONING REQUIRED  
**Blocker:** `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001`  
**Custody profile:** `CDX-CUSTODY-001`  
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

The runtime receives no Blob credential. GitHub Actions authenticates to the gateway using short-lived OIDC. The Vercel service uses Vercel OIDC for storage.

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

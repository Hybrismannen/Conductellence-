# CDX-WP04 — Independent SPETL Evidence Custody

**Status:** COMPLETE — INDEPENDENT REFERENCE CUSTODY VERIFIED  
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

WP04 closes only the **independent evidence-preservation** release criterion.

After observed reference-custody verification:
- independent preservation is `VERIFIED`;
- `satisfies_enforcing_requirement=true`;
- blocker #17 is removed from `core_release_blockers`;
- release remains `PRE_RELEASE`;
- enforcement remains `BOOTSTRAP` because repository protection and estate-runtime gates are separate.

## 8. Closure sequence

1. Merge custody implementation with blocker #17 still open.
2. Observe the main-branch producer workflow.
3. Observe a separate custodian workflow that reads and re-preserves the producer artifact.
4. Observe a separate verifier workflow that re-reads and verifies the custody artifact.
5. Capture run IDs, artifact IDs/digests, bundle/receipt/report hashes and negative-suite results.
6. Promote `CDX-CUSTODY-GHA-001` and independent preservation to `VERIFIED`.
7. Remove blocker #17 and rerun all CDX release gates.
8. Keep the long-lived Vercel target as a separate, stronger retention target when provisioning becomes available.


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

Historical target-specific action: restoring Vercel provisioning remains useful for the long-lived production custody target, but it is no longer required to satisfy the verified CDX reference-custody release gate.


## 10. Executable reference custody profile

WP04 now includes an independently executed reference profile, `CDX-CUSTODY-GHA-001`, without weakening the blocked long-lived Vercel target.

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

Producer, custodian and verifier are separate workflow runs. The custodian/verifier check out trusted `main` code, have no repository write permission, and do not execute producer-supplied code. The governed runtime receives no custodian storage-administrator credential.

The integrity chain combines the canonical SPETL event hash chain, custody-bundle SHA-256, custody-receipt SHA-256, immutable artifact digest and GitHub workflow-run provenance.

Reference artifacts retain for 90 days. Direct personal data is rejected by the reference custodian; pseudonymous subject references and explicit minimization metadata are required.

Human approval of the reference and long-lived profiles is recorded in `GOVERNANCE/orders/CDX-EVIDENCE-CUSTODY-APPROVAL-001.json`.

## 11. Verification gate

Merging this implementation does not close blocker #17.

Closure requires observed main-branch provenance for:
1. the producer workflow;
2. the separate custodian workflow;
3. the custody artifact ID and digest;
4. the separate verifier workflow;
5. the verification artifact ID and digest;
6. successful custody-package re-read and verification;
7. PASS evidence for ALLOW, DENY, policy unavailable, denied-effect contradiction, invalid event, tamper, withheld/loss, different runtime identity, forged authority and write/read/verify provenance.

Only after that observed chain may independent preservation move to `VERIFIED` and `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001` be removed. The Conductellence system remains `PRE_RELEASE` and `BOOTSTRAP` throughout WP04.


## 12. Observed verification and closure evidence

The approved reference profile was exercised from merged main commit `9aa8b034e82283a19e6e0106a7ef0ed8e5fdef15`.

| Evidence | Observed value |
|---|---|
| Producer workflow | `40782930399` — PASS |
| Producer artifact | `12857213700` |
| Producer artifact digest | `sha256:5a4658f301858067b27e6edbed14c398f4cb4db98641a3e74ece64933600cec7` |
| Custodian workflow | `40782954827` — PASS |
| Custody artifact | `12857114760` |
| Custody artifact digest | `sha256:22a8b97e50e6dec3f203135555f570576f68b13419d4c68d53ca1838a7a0462c` |
| Verifier workflow | `40782987339` — PASS |
| Verification artifact | `12857499066` |
| Verification artifact digest | `sha256:50b14a79fc3bb7b46611f5e32e0a1681c02149cb61e3b74e5ddcf3f3c6817f10` |
| Bundle | `CDX-BUNDLE-9D4792365BC245D28592DB6517F3109E` |
| Bundle hash | `sha256:0184925aff123ddd6bd8a83f147329ff3249f9462ccd936f7de639d0920929fc` |
| Custody receipt | `CDX-GHA-RCPT-912543631795420AA036980BDD7E2793` |
| Receipt hash | `sha256:6090c6fcb8b3392b98e5696d2858c63f444914b39e0c9726dfcf664e222c39d9` |
| Verification report | `CDX-GHA-VERIFY-80FA56D50B214E8E994EDE3E88C5EB55` |
| Verification report hash | `sha256:ead380c23a2e0f56ec688d45b609e9676e2c77c090cefcecd45fed59c38f1e73` |
| Events | 3: ALLOW, DENY, policy-unavailable SECURITY_STOP |

The producer run passed the canonical SPETL suite and custody suite, covering invalid event, tamper, withheld/lost evidence, forged authority, different runtime identity, denied-effect contradiction, source/run provenance and the positive ALLOW/DENY/policy-unavailable paths.

The verifier independently downloaded custody artifact `12857114760`, checked its platform digest, verified the event chain, bundle, receipt, source commit and custodian run identity, and emitted a separate PASS verification artifact.

**WP04 determination:** `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001` is satisfied for the CDX reference evidence pipeline and may be closed. The long-lived Vercel target remains an unprovisioned retention enhancement, not an open core-release evidence blocker.

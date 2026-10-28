# CDX-WP04 — RC-03 Independent SPETL Evidence Custody & Attestation

Status: IN EXECUTION — IMPLEMENTED PENDING OBSERVED VERIFICATION  
Date: 2026-10-28  
Blocker: `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001`

## 1. Purpose

WP04 closes the evidence-independence release blocker by moving SPETL from a repository-local hash-chain reference into an independently preserved evidence path that the evaluated runtime executor cannot freely rewrite or delete.

The closure rule remains strict:

> **Implementation is not verification. A custody design does not close the blocker until write, read, verification and negative evidence are actually observed outside the evaluated executor's unrestricted write capability.**

## 2. Canonical event contract

SPETL schema version `1.1` now requires the evidence elements specified by issue #17:

- event and timestamp identity;
- request ID, correlation ID and causation ID;
- actor and pseudonymous subject reference;
- authority and mandate references;
- policy reference, version/pin and digest;
- policy decision;
- attempted effect and observed effect status;
- run ID and trace reference;
- reviewer reference;
- explicit data-minimization metadata;
- control/evidence references;
- previous-event and event hashes.

Contradictory decision/effect combinations fail closed. A missing policy is represented by `policy_digest=UNAVAILABLE` and may not result in a permitted effect.

## 3. Approved custody principals

Human approval is recorded in:

`GOVERNANCE/orders/CDX-EVIDENCE-CUSTODY-APPROVAL-001.json`

Two profiles are distinguished.

### 3.1 CDX-CUSTODY-GHA-001 — executable reference custody

This is the reference profile that can be executed without giving the evaluated runtime a storage-administrator credential.

The chain is:

```text
SPETL Evidence Producer
        ↓ immutable producer artifact
separate workflow_run
SPETL Independent Custodian
        ↓ validated custody package + receipt
separate workflow_run
SPETL Custody Verifier
        ↓ verification report
GitHub Actions artifact service
```

Producer, custodian and verifier are separate workflow runs. The custodian and verifier check out trusted `main` code, have no repository write permission, and do not execute producer-supplied code. The custody package is bound by the SPETL event hash chain, bundle SHA-256 and custody receipt SHA-256. GitHub's artifact metadata supplies an additional platform artifact digest and workflow-run provenance.

The reference custody artifact retention is 90 days. Direct personal payload storage is prohibited by design; pseudonymous subject references and minimization metadata are used instead.

### 3.2 CDX-CUSTODY-001 — long-lived Vercel target

The existing Vercel custody service remains the stronger long-lived target:

- separate Vercel project;
- private Blob store;
- GitHub Actions OIDC sender authentication;
- source repository/ref/workflow claims;
- append-only/non-overwrite object path;
- authenticated read/verify endpoint;
- no delete API;
- governed tombstone/admin deletion policy.

The service implementation exists, but external provisioning is currently unavailable. WP04 therefore does not falsely call the Vercel profile verified.

## 4. Negative and adversarial requirements

The automated suite covers:

1. ALLOW;
2. DENY;
3. policy unavailable / fail closed;
4. denied write/effect contradiction;
5. missing/invalid event;
6. tampered bundle/event;
7. withheld or missing evidence;
8. different runtime identity;
9. forged authority;
10. source-commit and workflow-run provenance mismatch.

## 5. Credential and key lifecycle

The reference profile uses no user-managed long-lived custody signing key.

Its trust root is the separate GitHub workflow-run identity plus immutable artifact service metadata. Job-scoped platform credentials are not shared with the evaluated runtime across workflow runs.

The Vercel target similarly keeps the Blob project binding inside the custody project rather than distributing a storage administrator credential to the governed runtime.

## 6. Retention, deletion and rights

The reference profile uses 90-day platform retention. If evidence must survive longer, it must be exported to an approved long-lived custody profile before expiry.

The long-lived target policy uses governed disposition: no public delete endpoint, explicit authority/reason, privacy/legal review where applicable, and a non-content tombstone where lawful.

## 7. External provisioning observation

An attempt to provision the separate Vercel project was made during WP04. The provider currently does not permit new resource creation for the team. The repository records this only as `EXTERNAL_RESOURCE_CREATION_UNAVAILABLE`; no financial/account detail is committed.

This does not prevent the executable cross-workflow reference custody profile from being tested independently.

## 8. Promotion rule

Before the blocker can close, the reference profile must be merged and then produce an actual main-branch chain with:

- successful producer run;
- successful separate custodian run;
- custody artifact ID/digest;
- successful separate verifier run;
- verification artifact ID/digest;
- downloaded/inspected custody receipt and verification report;
- all negative tests PASS.

Only then may:

- `SPETL/evidence-preservation-state.json` move to `VERIFIED`;
- `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001` be removed from core-release blockers;
- issue #17 close.

No other maturity axis is promoted by WP04.

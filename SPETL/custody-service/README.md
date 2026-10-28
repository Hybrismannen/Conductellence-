# CDX SPETL Independent Custody Service

This directory is the deployment unit for `CDX-CUSTODY-001`, implementing the existing SPETL independent-preservation obligation. It is not a new CDX subsystem and does not change the RC-01 boundary.

## Trust separation

The governed runtime does not receive Vercel Blob credentials. A trusted GitHub Actions workflow authenticates to the custody gateway using a short-lived GitHub OIDC token. The custody project accesses its private Blob store using Vercel OIDC.

The service exposes:
- `POST /api/v1/evidence` — validate and append a custody bundle to a unique, non-overwritable private Blob pathname;
- `POST /api/v1/verify` — authenticated origin-consistent read and digest/hash-chain verification;
- `GET /api/health` — non-sensitive service state.

There is deliberately no delete or update endpoint.

## Production trust conditions

Default accepted identity:
- repository: `Hybrismannen/Conductellence-`
- ref: `refs/heads/main`
- workflow: `Hybrismannen/Conductellence-/.github/workflows/spetl-evidence-publish.yml@refs/heads/main`
- audience: `cdx-spetl-custody`

These may be overridden only through custody-project configuration; the runtime itself must not receive storage-administration credentials.

## Storage semantics

Evidence paths are derived from date, bundle ID and SHA-256 digest. `allowOverwrite:false` is mandatory. Private Blob origin reads use `useCache:false` for verification.

Administrative deletion is outside the application API and is governed by the custody policy. If deletion is legally required, it must be separately authorized and leave a non-content tombstone where lawful.

## Closure rule

Deployment alone does not close `CDX-BLOCK-EVIDENCE-INDEPENDENCE-001`. Closure requires observed external tests for allow, deny, policy-unavailable, denied write, invalid event, tamper, withheld/lost evidence, different runtime identity and forged authority.

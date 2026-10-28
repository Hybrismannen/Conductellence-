# SPETL — Security Penetration, Execution & Traceability Ledger

**System ID:** `CDX-SYS-002`  
**Canonical reference runtime:** `SPETL/spetl.py`

SPETL is the Conductellence evidence plane. Runtime decisions are recorded as append-oriented events with correlation, causation, authority, policy and control evidence.

The canonical reference runtime:

- appends JSONL events;
- links each event to the prior event hash;
- verifies the resulting hash chain;
- treats corrections as new events rather than rewriting prior evidence.

`SPETL/spetl.py` is the only canonical reference implementation in this repository.

Production deployments should preserve the same event semantics in an independently controlled evidence store. Git history and the local reference runtime do not, by themselves, constitute independent production evidence preservation.


## Independent custody profile — CDX-CUSTODY-001

WP04 adds an implementation target under `SPETL/custody-service` for independent preservation in a separate Vercel project/private Blob store. It uses short-lived GitHub OIDC for source authentication and Vercel OIDC for storage access. The governed runtime does not receive Blob administration credentials and the service exposes no delete/update endpoint.

See:
- `SPETL/custody/custody-policy.json`
- `SPETL/custody/deployment-state.json`
- `SPETL/schemas/custody-bundle.schema.json`
- `PROGRAMME/WP04-INDEPENDENT-SPETL-EVIDENCE-CUSTODY.md`

The blocker remains open until external provisioning and verification are observed.


## Canonical custody event contract

SPETL custody schema version `1.1` requires request/correlation/causation identity, authority and mandate references, policy reference/version/digest, decision, attempted effect and effect status, run/trace identity, reviewer reference, pseudonymous subject reference, data-minimization metadata and the event hash chain.

A policy-unavailable event must fail closed; it cannot record a permitted effect.

## Independent custody profiles

WP04 defines two approved custody profiles:

- `CDX-CUSTODY-GHA-001` — executable reference custody using three separate GitHub workflow runs (producer → custodian → verifier) with immutable Actions artifacts, SHA-256 custody receipts and 90-day reference retention.
- `CDX-CUSTODY-001` — long-lived Vercel private-Blob custody target with GitHub OIDC source authentication, non-overwrite writes and authenticated read/verify.

The reference profile may satisfy the core release evidence-independence gate only after actual workflow/artifact provenance is observed and recorded. Source code or local tests alone do not close the blocker.

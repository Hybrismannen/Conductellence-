# CDX-EVID-001 — Scientific Evidence & Epistemic Assurance

**System ID:** `CDX-EVID-001`  
**Parent authority:** `CDX-SYS-001` Conductellence  
**External provider:** Scite (provider adapter; not authority)  
**Status:** BOOTSTRAP_IMPLEMENTED

## Function

CDX-EVID-001 governs scientific and scholarly evidence used to justify, interpret, test, challenge or revise Conductellence doctrine, controls and technical architecture.

It is structurally separate from the legal authority layer.

```text
LAW / PRIMARY LEGAL SOURCES
        ↓
Legal Authority / Legal Resolver
        ↓
Conductellence obligations
```

and:

```text
SCIENTIFIC LITERATURE / SCITE
        ↓
Evidence Authority
        ↓
claims / rationale / controls / tests
```

Scientific evidence may change **knowledge state**. It may not change **authority state**.

## Core invariants

1. A paper is not a claim.
2. A citation is not support.
3. Citation count is not truth.
4. Scite's supporting/contrasting/mentioning label is evidence metadata, not a Conductellence verdict.
5. A paper's existence does not establish contextual applicability.
6. Retraction/correction/concern events degrade evidence state; they do not silently rewrite historic decisions.
7. No Scite result may create, amend or repeal Conductellence law.
8. No Scite result may create legal applicability.
9. Every stronger evidence relationship must be bound to a claim-evidence record.
10. Evidence ingestion shall be credit-aware and cache-first.

## Evidence states

`UNSOURCED → SOURCED → CORROBORATED → CONTESTED → ROBUST → DEGRADED → SUPERSEDED → RETRACTED`

These states are governance states. They are not inferred from citation counts alone.

## Credit-efficient provider strategy

Conductellence uses Scite only when needed:

- **Exact DOI metadata lookup first** when DOI is known.
- **Broad discovery searches** only for an explicit research question, default max 10 results.
- **Citation graph** only after a seed paper is admitted and topology materially helps.
- **Full-text reading** only for shortlisted papers.
- **Editorial/retraction checks** refresh more often than citation tallies.
- **No scheduled Scite search workflow.**
- **No duplicate fetch when a fresh local cache exists.**
- One master Scite Collection; domain classification stays local.

## Architecture

```text
evidence request
    ↓
local cache?
 ┌──yes──→ use cached provider evidence
 │
 no
 ↓
budget/admission gate
 ↓
Scite adapter
 ↓
provider observation
 ↓
Scientific Evidence Registry
 ↓
Claim-Evidence Binding
 ↓
Evidence state / contradiction / drift
 ↓
SPETL / Security Twin / Control rationale
```

## Provider boundary

Scite is an external evidence provider. All returned data remains `UNTRUSTED_EXTERNAL_EVIDENCE` until registered.

The adapter may:
- discover papers;
- retrieve DOI metadata;
- retrieve indexed excerpts/full text where permitted;
- retrieve Smart Citation metadata;
- traverse citation graphs;
- identify editorial notices;
- manage the single governed Scite collection.

The adapter may not:
- grant authority;
- decide legal applicability;
- amend law;
- autonomously declare a scientific claim true;
- autonomously promote a claim to ROBUST;
- delete adverse or contrasting evidence.

## Canonical files

- `provider/scite-policy.json`
- `registry/publications.json`
- `registry/claims.json`
- `registry/claim-evidence-bindings.json`
- `registry/evidence-drift.json`
- `schemas/claim-evidence-binding.schema.json`
- `AUDITS/audit_evidence_authority.py`

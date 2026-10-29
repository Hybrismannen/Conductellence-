# CDX-WP08 — Estate Registry v2 Applicability Classification

**Status:** COMPLETE — APPLICABILITY CLASSIFIED  
**Registry:** `CDX-ESTATE-REGISTRY-V2`  
**Observed:** 2026-10-29  
**Source baseline:** `ce7dde1bf147d1a5e762fabf3395198055927055`

## 1. Objective

WP08 performs the full estate census and applicability classification reserved outside the CDX 1.0 core-release boundary.

The required topology is:

```text
31 known repository identifiers
→ identity / alias normalization
→ 30 unique current repository objects
→ CDX applicability classification
→ canonical-anchor requirement
→ runtime-screening posture
→ WP09 migration handoff
```

WP08 does **not** install downstream anchors, verify runtime effects or promote estate enforcement.

## 2. Result

The live GitHub estate was reconciled across the `Hybrismannen` and `Motherpher` owners.

Registry v2 contains exactly:

- **31** known repository identifiers;
- **30** unique current repository objects;
- **1** CDX authority source;
- **28** current governed/applicable consumer repositories;
- **1** current explicit exclusion;
- **1** historical alias record.

Canonical register:

`ESTATE-REGISTRY/registry-v2.json`

## 3. Explicit identity normalization

`Hybrismannen/form-flode` and `Motherpher/form-flode` resolve to the same GitHub repository object:

`repository_id = 1379622813`

Treatment:

- `Hybrismannen/form-flode` — historical alias/provenance only;
- `Motherpher/form-flode` — current canonical FFC repository;
- the historical path must not be counted as a second current repository;
- FFC remains `UNBOUND` on current `main` pending canonical identity/anchor migration.

## 4. Explicit exclusion

`Hybrismannen/Barnombudet` is classified:

`EXCLUDED_BY_DECISION`

This implements decision D-017. Barnombudet must not receive a CDX dependency merely because it is visible in the same GitHub estate.

Its WP09 action is therefore `NONE`.

## 5. Applicability versus runtime

WP08 separates three questions that must not be collapsed:

```text
repository is in governed estate?
        ↓
canonical .cdx anchor required?
        ↓
does CDX-RUNTIME-001 apply to consequential execution?
```

A governed repository can require a canonical CDX anchor while having no current consequential runtime.

Runtime screening values in Registry v2 are therefore triage classes, not runtime-verification states.

No WP08 record claims:

- `VERIFIED_RUNTIME_BOUND`;
- production consequential enforcement;
- estate-wide `ENFORCING`.

## 6. Canonical anchor baseline

Direct live reads of current default branches found canonical `.cdx/anchor.json` only in:

- `Motherpher/FFOS` — `CDX_CI_MONITORED`;
- `Hybrismannen/pius-universe` — `ANCHOR_DECLARED`.

Both are still pinned to a pre-release CDX commit and must be repinned/reverified against released CDX 1.0.0 during WP09/WP10.

The other **26 governed/applicable consumer repositories** do not currently carry the canonical anchor on `main`.

Legacy `.security/conductellence.json` material is preserved as provenance and migration evidence where present. It is not treated as a canonical anchor.

## 7. WP09 migration classes

Registry v2 assigns a deterministic WP09 action to every governed current repository:

- `REPIN_TO_RELEASE_AND_REVERIFY` — existing canonical anchors;
- `INSTALL_AND_RECONCILE_IDENTITY` — FFC;
- `MIGRATE_LEGACY_TO_CANONICAL` — valid legacy binding evidence;
- `INSTALL_CANONICAL_ANCHOR_REPAIR_STALE_LEGACY_CLAIM` — stale RFSU public binding claim;
- `INSTALL_CANONICAL_ANCHOR` — newly classified governed repositories without legacy binding.

Every governed/applicable current repository also carries:

`wp10_action = VERIFY_AFTER_WP09`

## 8. Audit controls

WP08 extends:

- `AUDITS/audit_estate_registry.py`;
- `ESTATE-REGISTRY/verify-cdx-registry.py`.

The audits fail if:

- the 31/30 topology changes silently;
- Barnombudet loses its explicit exclusion;
- the Form & Flöde historical alias becomes a second current repository;
- a governed current repository does not require an anchor;
- a governed repository lacks a WP09/WP10 handoff;
- Registry v2 invents a verified runtime state;
- WP08 removes `CDX-BLOCK-ESTATE-RUNTIME-001`;
- WP08 promotes `estate_integration_state`.

## 9. State after WP08

WP08 changes the programme classification layer only.

Canonical state remains:

- constitutional: `ADOPTED`;
- core runtime: `VERIFIED_REFERENCE_RUNTIME`;
- release: `RELEASED`;
- enforcement: `BOOTSTRAP`;
- estate integration: `PENDING_RUNTIME_BINDINGS`;
- estate runtime blocker: `CDX-BLOCK-ESTATE-RUNTIME-001`.

## 10. Handoff

**Next:** `CDX-WP09 — Canonical Anchor Migration`.

WP09 may now operate from the complete Registry v2 migration queue. It must not treat registry inclusion as proof of anchor installation or runtime enforcement.

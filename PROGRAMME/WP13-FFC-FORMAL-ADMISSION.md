# CDX-WP13 — FFC Formal Admission

**Status:** COMPLETE — FORMALLY ADMITTED  
**Date:** 2026-10-30  
**Canonical repository:** `Motherpher/form-flode`  
**System ID:** `FFC`

## Purpose

WP13 formally admits FFC into the CDX estate under its canonical current repository identity. It resolves the historical repository-name migration without creating a duplicate system and preserves runtime verification as a separate axis.

## Admission evidence

The current GitHub repository is `Motherpher/form-flode`, repository ID `1379622813`. The historical path `Hybrismannen/form-flode` redirects to that same repository object and is retained only as provenance.

The current canonical anchor is:

- path: `.cdx/anchor.json`
- blob: `9b9fa1de1ea63ea746148c1eb7d8d7fedbc3df00`
- state: `CDX_BOUND`
- verification: `PASS`
- CDX release: `1.0.0`
- policy blob: `55dbcdac2f822b59a5a5f0f19eeadfa61d2c7ed0`

The anchor blob is unchanged from the WP10 verified reconciliation commit `ea4f2db7129b2509bfdc487ee8e19f30d6a74f1c`.

## Canonical result

`Motherpher/form-flode` moves from pending admission to the admitted estate registry as system `FFC`.

`Hybrismannen/form-flode` / `CDX-EST-001` remains a historical alias record and is not a second current repository.

## Runtime boundary

Formal admission does not promote FFC runtime state.

- runtime integration: `NOT_VERIFIED`
- consequential enforcement: `false`
- production effect authorization: `false`

The legacy reference-runtime files remain historical evidence and do not override the canonical anchor runtime state.

## State effect

WP13 advances only the FFC identity/admission axis.

- estate integration remains `BINDINGS_IN_PROGRESS`
- estate enforcement remains `BOOTSTRAP`
- estate runtime blocker remains open
- WP11 FFOS blocker remains open
- WP14 remains the estate-wide propagation/closure stage

**Next target:** `CDX-WP14`.

## Validation note

The central estate-registry reconciliation validator was updated for the WP13 admitted state; it continues to reject runtime promotion from formal admission.

# CDX-WP09 — Canonical Anchor Migration

**Status:** COMPLETE — 28/28 GOVERNED CONSUMERS MIGRATED  
**Target release:** `CDX 1.0.0`  
**Completed:** 2026-10-29  
**Evidence:** `ESTATE-REGISTRY/wp09-migration-evidence.json`

## 1. Objective

WP09 migrates every current governed consumer repository identified by Registry v2 to the canonical CDX local anchor:

`.cdx/anchor.json`

The migration binds repository governance to the immutable released CDX version without claiming independent verification or consequential runtime enforcement.

## 2. Migration contract

Every migrated consumer anchor now uses:

- schema: `cdx.anchor/v1`;
- binding mode: `PINNED_RELEASE`;
- release ref: `1.0.0`;
- policy digest: `git-blob-sha1:55dbcdac2f822b59a5a5f0f19eeadfa61d2c7ed0`;
- binding state: `ANCHOR_DECLARED`;
- verification state: `NOT_VERIFIED`.

This is a declaration and version pin. WP10 performs independent verification.

## 3. Result

Registry v2 identified **28 current governed consumer repositories**. WP09 migrated **28/28**.

Independent GitHub reads after merge confirmed the anchor on every consumer default branch.

Migration classes completed:

- existing canonical anchors repinned from pre-release commit state to released CDX 1.0.0;
- legacy Conductellence bindings migrated to the canonical anchor while retaining legacy files as provenance;
- newly classified repositories received their first canonical CDX anchor;
- FFC identity migration established the current `Motherpher/form-flode` anchor while preserving `Hybrismannen/form-flode` as historical alias only.

## 4. Explicit exclusion

`Hybrismannen/Barnombudet` remains `EXCLUDED_BY_DECISION`.

WP09 made no CDX anchor or dependency change to that repository.

## 5. FFC boundary

`Motherpher/form-flode` now carries the canonical release-pinned anchor on `main`.

This completes the WP09 technical identity/anchor migration but does **not** complete FFC admission.

FFC remains:

- anchor: `ANCHOR_DECLARED`;
- verification: `NOT_VERIFIED`;
- WP10 action: independent anchor verification;
- WP13 action: FFC admission.

The historical `Hybrismannen/form-flode` record remains provenance only.

## 6. FFOS boundary

FFOS is now pinned to CDX 1.0.0 and its anchor verification has been reset to `NOT_VERIFIED`.

Its runtime axis remains separately:

`BOUND_PENDING_RUNTIME_INTEGRATION`

WP09 does not advance FFOS runtime binding. That belongs to WP11.

During WP09, FFOS also exposed a pre-existing GitHub Actions execution regression that had begun on unrelated AMA changes before the WP09 migration. The anchor migration itself was therefore accepted through exact default-branch readback, without converting CI failure into a false runtime or verification claim. WP10 must independently verify the repository anchor.

## 7. Pius boundary

Pius Universe was repinned to released CDX 1.0.0. Its live anchor validators were updated to distinguish the current release anchor from preserved historical P5 pre-release observations.

Pius remains:

- anchor: `ANCHOR_DECLARED`;
- verification: `NOT_VERIFIED`;
- reference repository runtime evidence: separate from estate verification;
- dedicated binding verification: WP12 after WP10 estate reconciliation.

## 8. State discipline

WP09 does not establish:

- `CDX_BOUND`;
- `CDX_CI_MONITORED` as newly verified estate state;
- `VERIFIED_RUNTIME_BOUND`;
- estate-wide `ENFORCING`.

Canonical CDX axes remain:

- constitutional: `ADOPTED`;
- core runtime: `VERIFIED_REFERENCE_RUNTIME`;
- release: `RELEASED`;
- enforcement: `BOOTSTRAP`;
- estate integration: `PENDING_RUNTIME_BINDINGS`.

`CDX-BLOCK-ESTATE-RUNTIME-001` remains open.

## 9. Handoff

**Next:** `CDX-WP10 — Estate Anchor Verification & Reconciliation`.

WP10 must independently re-read and verify every migrated anchor against Registry v2 and the CDX 1.0.0 release contract before any repository is promoted beyond `ANCHOR_DECLARED`.

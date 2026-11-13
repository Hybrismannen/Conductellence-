# Estate admission candidates — 2026-11-13

**Status:** DIRECTOR-APPROVED ESTATE APPLICABILITY / TECHNICAL BINDING UNVERIFIED · **Authority:** Director decision 2026-11-13 · **Existing registry:** [registry-v2.json](registry-v2.json)

## Director admission decision

On 2026-11-13 the Director explicitly decided: **CDX is the control system for both**. See [prospective machine-readable estate admission](estate-admissions-2026-11-13.json). This accepts CDX governance applicability for both domains; it does not imply CI or runtime verification.

## Candidate local hooks

| Repository | Local PR | Anchor state | Existing registry state | Recommended next action |
|---|---|---|---|---|
| `Motherpher/Ideburen` | [#1](https://github.com/Motherpher/Ideburen/pull/1), merged | `ANCHOR_DECLARED` | Director admitted via prospective addendum; not historical registry v2 | Verify schema/pin, CI and applicable runtime controls |
| `Hybrismannen/Opal-Sense-I` | [#18](https://github.com/Hybrismannen/Opal-Sense-I/pull/18), merged | `ANCHOR_DECLARED` | Director admitted via prospective addendum; not historical registry v2 | Verify schema/pin, CI and applicable runtime controls |

These declarations use the canonical `cdx.anchor/v1` schema, `CDX-LAW-001`, `CDX-GOV-ANCHOR-001`, and release `1.0.0` with the verified prior WP10 digest `git-blob-sha1:55dbcdac2f822b59a5a5f0f19eeadfa61d2c7ed0`. **The previous digest was verified for the historical WP10 set, not for these new anchors**. Their validity is not presumed.

## Explicit exclusion preserved

`Hybrismannen/Barnombudet` remains **EXCLUDED_BY_DECISION** per D-017: no CDX anchor, synchronization, dependency or control. Do **not** add a local anchor or interpret a general "all repositories" instruction as overturning this specific ruling.

## Reconciliation / no duplicate work

An accessible-repository readback on 2026-11-13 found valid-looking existing `.cdx/anchor.json` files in the other sampled estate repositories, including FFC, FFOS, FF-Spatial, Politent, UDL, GreenBell, BDNA, Re-Eco, Pius, F&F DNA and other research/project archives. **Anchor present** is not the same as current conformance or runtime verification. No existing anchor was overwritten.

The reference CDX registry v2 is a dated estate baseline; adding newer repositories requires source-specific registration, not a fabricated rewrite of its historical membership counts.

## Admission work still required

1. Review the two local PRs; confirm that each domain is eligible for governance without overriding contracts, editorial autonomy or IP rights.
2. Add reviewed entries to the **current** central CDX estate registry with stable record IDs and evidence. Do not mutate the 2026-10-29 snapshot as though the new repositories were historically present.
3. Independently verify exact repository identities, local merged anchor contents, schema and policy-pin digest; retain evidence and synchronization reference.
4. Design or confirm local CI and, only where consequential runtime exists, policy-gated local enforcement with explicit authority and mandate, failure-closed behavior, and SPETL evidence.
5. Advance from `ANCHOR_DECLARED` to `CDX_BOUND` or runtime states solely upon evidence and Director-approved promotion.

**This document is a candidate intake record; it does not itself constitute canonical registry admission or enforcement.**

## Current interpretation

The two local anchors were merged into main and read back. The Director approved applicability. CI and runtime evidence remain unverified and require separate acceptance; D-017 Barnombudet exclusion remains unchanged.

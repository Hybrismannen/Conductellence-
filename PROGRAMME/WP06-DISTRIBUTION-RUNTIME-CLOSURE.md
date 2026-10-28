# CDX-WP06 — Distribution Package & CDX-RUNTIME-001 Closure

**Status:** RELEASE CANDIDATE PACKAGED FOR REVIEW  
**Runtime contract:** `CDX-RUNTIME-001`  
**Target:** CDX 1.0 release candidate  
**Date:** 2026-10-28

## 1. Purpose

WP06 closes the distribution and runtime-contract layer of the frozen CDX 1.0 core. It does not release CDX and does not perform estate propagation.

The distinction is:

```text
distributable, pinned, tested candidate
≠
RELEASED
≠
VERIFIED_RUNTIME_BOUND in a consumer
≠
estate ENFORCING
```

## 2. Compatibility defect found and repaired

WP04 hardened SPETL to event schema v1.1. During WP06 review, the canonical policy engine was found still referencing the removed `SPETL/ledger.py` path and emitting the older evidence shape.

That made the runtime/distribution layer internally inconsistent.

WP06 repairs the contract so both the canonical policy engine and portable distribution runtime emit SPETL v1.1 with:

- explicit authority + mandate;
- policy version + SHA-256 policy digest;
- run/correlation/causation/trace identity;
- attempted effect and effect status;
- minimization metadata;
- full control results and evidence references.

## 3. Canonical binding moves to the CDX anchor

The portable 1.0 runtime now treats:

`.cdx/anchor.json`

as the canonical binding source.

The legacy `.security/conductellence.json` manifest is not accepted as a substitute for canonical CDX 1.0 binding.

This does not migrate downstream repositories now; WP09 remains the estate migration stage.

## 4. Machine-readable runtime contract

WP06 adds `RUNTIME-INTEGRATION/CDX-RUNTIME-001.json`.

The contract freezes:

- authority/mandate requirements;
- anchor continuity;
- fail-closed decision behavior;
- SPETL v1.1 evidence;
- local enforcement ownership;
- required allow/deny/policy-unavailable testing;
- separation between repository binding, reference runtime and application runtime verification.

## 5. Release-candidate package

After the runtime consistency audit passes, WP06 creates a reproducible candidate manifest under:

`DISTRIBUTION/releases/1.0.0-rc1/`

The package pins source artifact Git blob SHAs and target install paths. It is a candidate package only. WP07 may convert it into a release only when all core release blockers are actually closed. At WP06 closure those blockers were #5 and #17; WP04 subsequently verified and closed #17.

## 6. Runtime acceptance

`AUD-CDX-RUNTIME-DISTRIBUTION-001` verifies:

1. canonical/distribution policy identity;
2. all 69 control self-tests;
3. canonical engine SPETL v1.1 emission;
4. portable runtime SPETL v1.1 emission;
5. actual policy-unavailable SECURITY_STOP with BLOCKED evidence;
6. canonical `.cdx/anchor.json` binding;
7. the machine-readable runtime contract.

## 7. State discipline

WP06 may reach `RUNTIME_CONTRACT_CLOSED / RELEASE_CANDIDATE_PACKAGED` while:

- release remains `PRE_RELEASE`;
- enforcement remains `BOOTSTRAP`;
- at WP06 closure, WP04 blocker #17 was still open;
- WP05 blocker #5 remains open.

No distribution artifact may erase those external gates.


## 8. WP06 closure result

The WP06 candidate now consists of:

- frozen machine-readable `CDX-RUNTIME-001 v1.0.0`;
- canonical and portable runtimes aligned to SPETL v1.1;
- canonical `.cdx/anchor.json` binding requirement;
- reproducible package builder;
- `CDX-DIST-1.0.0-RC1` manifest with exact Git blob pins;
- release gate that initially preserved blockers #5 and #17; WP04 subsequently closed #17 through verified reference custody.

If the WP06 PR passes all CDX gates, WP06 is complete as:

`RUNTIME_CONTRACT_CLOSED / RELEASE_CANDIDATE_PACKAGED`

This does not authorize release. WP07 remains blocked until every remaining core gate is closed; after WP04 verification, #5 repository protection is the remaining core-release blocker.

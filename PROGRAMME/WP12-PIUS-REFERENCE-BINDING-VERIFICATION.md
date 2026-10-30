# CDX-WP12 — Pius Reference Consumer Binding Verification

**Status:** COMPLETE — REFERENCE BINDING VERIFIED  
**Date:** 2026-10-30  
**Consumer:** `Hybrismannen/pius-universe` / `CDX-EST-003`  
**Governing contract:** `CDX-RUNTIME-001@1.0.0`

## 1. Purpose

WP12 independently verifies the Pius consumer relationship from the CDX authority repository. It closes the Pius **reference-consumer** verification stage without modifying the Pius repository and without converting repository CI into a claim of consequential application-runtime mediation.

The accepted state is:

`VERIFIED_REFERENCE_RUNTIME_REPOSITORY_CI_ONLY`

It is explicitly **not**:

`VERIFIED_RUNTIME_BOUND`

## 2. Independent readback

WP12 observed Pius Universe main at:

`1f7ee643c275bb2e3825f2e204b34f30da5df801`

The canonical anchor is `CDX_BOUND / PASS`, pinned to CDX release `1.0.0` and policy blob `55dbcdac2f822b59a5a5f0f19eeadfa61d2c7ed0`.

The existing Pius reference-runtime declaration is limited to `REPOSITORY_CI`. Its runtime source, policy, runtime-integration declaration and reference binding workflow are byte-identical to the versions exercised successfully by GitHub Actions run `40895924794`, which passed binding check, self-test and policy-unavailable test.

## 3. Current downstream CI drift

After WP10 promoted the Pius anchor from `ANCHOR_DECLARED` to the independently verified `CDX_BOUND` state, the Pius-local precheck began failing because its unchanged script still asserts:

`binding_state == ANCHOR_DECLARED`

Runs `40902456178` and `40902456160` therefore fail on a stale pre-WP10 invariant before executing the reference checks.

WP12 records this as downstream CI drift. It does not modify Pius and does not treat that stale assertion as a failure of the unchanged reference runtime.

## 4. CDX-owned consumer profile

WP12 admits:

`RUNTIME-INTEGRATION/consumers/CDX-PIUS-CONSUMER-001.json`

This profile binds Pius reference consumption to released `CDX-RUNTIME-001@1.0.0`, preserves human-sovereign authority, requires explicit authority and mandate, and leaves every local effect gate owned by Pius.

The profile grants no execution authority and authorizes no downstream mutation.

## 5. Consequential-runtime boundary

The Pius preparation inventory currently records:

- operational consequential effect endpoints: **0**
- installed effect guards: **0**
- verified runtime effects: **0**

Therefore WP12 does not and cannot claim application-runtime mediation. Future effectful Pius runtime requires actual local enforcement, current pin/revocation checks, ALLOW/DENY/POLICY_UNAVAILABLE effect tests, SPETL v1.1 evidence and independent verification before any `VERIFIED_RUNTIME_BOUND` state.

## 6. Construction-entry consequence

The CDX-side foundation required for a later Pius construction-entry review is now present:

1. CDX 1.0.0 is released;
2. native CDX repository protection is verified;
3. independent reference custody is verified;
4. a versioned CDX/Pius consumer profile is admitted.

The resulting state is:

`READY_FOR_SEPARATE_DIRECTOR_REVIEW`

This is not Pius construction authorization, activation or deployment.

## 7. State discipline

WP12 advances only the Pius reference-runtime axis:

- Pius anchor: `CDX_BOUND / PASS`
- Pius reference runtime: `VERIFIED_REFERENCE_RUNTIME`
- Pius consequential enforcement: `false`
- estate integration: remains `BINDINGS_IN_PROGRESS`
- estate enforcement: remains `BOOTSTRAP`
- `CDX-BLOCK-ESTATE-RUNTIME-001`: remains open
- WP11 FFOS blocker: unchanged
- FFC admission: remains WP13
- estate-wide propagation: remains WP14

**Next programme target:** `CDX-WP13 — FFC Formal Admission`.

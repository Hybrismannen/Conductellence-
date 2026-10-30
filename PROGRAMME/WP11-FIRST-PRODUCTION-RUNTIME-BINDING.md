# CDX-WP11 — First Consequential Runtime Binding (FFOS)

**Status:** IMPLEMENTATION STAGED — VERIFICATION BLOCKED AT GITHUB ACTIONS  
**Consumer:** `Motherpher/FFOS`  
**Contract:** `CDX-RUNTIME-001@1.0.0`  
**Current implementation PR:** `Motherpher/FFOS#35`  
**Superseded implementation:** `Motherpher/FFOS#29`

## Objective

Verify the first real FFOS consequential application-runtime effect under the released CDX runtime contract without conflating repository anchoring, implementation, runtime verification, deployment or estate-wide enforcement.

A Vercel deployment is **not** part of the WP11 acceptance contract.

## Current implementation

FFOS PR #35 rebuilds the binding against current FFOS `main` and stages:

- immutable CDX 1.0 policy, runtime-contract and SPETL pins;
- fail-closed CDX policy integrity and decision evaluation;
- the real Director-session issuance effect gate;
- a separate non-privileged runtime-proof HTTP effect;
- SPETL 1.1 PRE_EFFECT, BLOCKED and POST_EFFECT evidence;
- ALLOW, DENY and POLICY_UNAVAILABLE → SECURITY_STOP acceptance paths;
- real HTTP assertions that an effect occurs only after permissive CDX evaluation;
- explicit proof that restrictive/unavailable-policy paths produce no effect.

The staged anchor remains:

`CDX_RUNTIME_GUARDED / RUNTIME_GUARDED_UNVERIFIED`

No agent activation is implied. Household Family and other agents remain governed by their own lifecycle/acceptance state.

## Verification model

Runtime verification is deployment-independent.

The required evidence chain is:

```text
exact FFOS implementation
→ successful build
→ real HTTP runtime starts
→ ALLOW produces bounded effect
→ DENY produces no effect
→ POLICY_UNAVAILABLE produces SECURITY_STOP and no effect
→ SPETL PRE_EFFECT / BLOCKED / POST_EFFECT evidence
→ reviewed merge to FFOS main
→ exact merged-main re-verification
→ independent CDX reconciliation
```

This is sufficient for the FFOS runtime claim because `CDX-RUNTIME-001` requires consequential-effect mediation evidence; it does not require a Vercel deployment.

## Current blocker

### FFOS GitHub Actions execution

Fresh PR #35 workflow runs still fail before any runner step executes.

Observed characteristics:

- workflow jobs are created;
- each job concludes `failure`;
- `steps = null`;
- `logs_url = null`;
- no checkout, build, test or runtime command starts.

Therefore the failures are execution-infrastructure failures, not failed runtime assertions.

Canonical blocker:

`FFOS-GHA-RUNNER-001`

## State discipline

While this blocker exists:

- FFOS remains `CDX_BOUND / PASS` on the repository-anchor axis;
- staged runtime remains `RUNTIME_GUARDED_UNVERIFIED`;
- CDX estate integration remains `BINDINGS_IN_PROGRESS`;
- CDX enforcement remains `BOOTSTRAP`;
- `CDX-BLOCK-ESTATE-RUNTIME-001` stays open;
- `CDX-BLOCK-WP11-FFOS-EXECUTION-001` stays open.

No deployment blocker is part of WP11.

## Completion gate

WP11 can close when:

1. GitHub Actions can execute runner steps for the exact current PR #35 implementation;
2. static acceptance and production build pass;
3. the HTTP runtime exercises ALLOW, DENY and POLICY_UNAVAILABLE cases;
4. SPETL runtime evidence is preserved;
5. reviewed implementation is merged to current FFOS `main`;
6. the exact merged main commit is re-verified;
7. independent CDX reconciliation promotes FFOS to `CDX_RUNTIME_VERIFIED / VERIFIED_RUNTIME_BOUND`.

Once one consequential governed runtime is independently verified, the estate integration axis may be reconsidered for `PARTIALLY_BOUND`. Estate-wide `ENFORCING` does not follow automatically.

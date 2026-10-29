# CDX WP11 — FFOS Estate runtime admission boundary

**Status:** ENGINEERING CANDIDATE / NOT LIVE RUNTIME VERIFIED  
**Authority:** CDX-SYS-001; contract `CDX-RUNTIME-001` v1.0.0  
**Estate policy:** `CDX-ESTATE-TERMS-001`  
**Consumer:** `Motherpher/FFOS` (system `FFOS`)  
**Source observation:** 2026-10-29

## Verified starting point

CDX release 1.0.0 is published. WP08 identifies 28 `GOVERNED_APPLICABLE` current consumers, one authority source, one excluded current repository (`Hybrismannen/Barnombudet`), and one historical alias. WP09 migrated 28 canonical anchors. WP10 independently verified **28/28** local anchor identities, release pins, policy digests and registry correspondence in `ESTATE-REGISTRY/wp10-anchor-verification-evidence.json`; the evidence expressly advances **the anchor axis only**. WP10 does **not** establish runtime effect mediation, live custodial evidence, or Estate-wide `ENFORCING`.

FFOS `.cdx/anchor.json` on main is release pinned (`PINNED_RELEASE`, `1.0.0`, `git-blob-sha1:55dbcdac2f822b59a5a5f0f19eeadfa61d2c7ed0`) and now records `CDX_BOUND` with anchor verification PASS, but `conformance.runtime_state` remains `BOUND_PENDING_RUNTIME_INTEGRATION`. The stale historical snapshot in `GOVERNANCE/system-state.json` must not override the more specific WP10 evidence or the current consumer anchor.

## WP11 admission and mediation contract

1. **Host-resolved membership**: the consumer host must independently resolve its canonical repository and GitHub repository identity, verify the current signed or otherwise independently authenticated CDX Estate Registry and apply `GOVERNED_APPLICABLE`. An agent-supplied realm or an external label cannot exempt a current Estate consumer. Exclusions and historical aliases remain authoritative in CDX.
2. **Verified anchor continuity**: read and verify the consumer-local `.cdx/anchor.json` identity, release pin, policy digest, verified anchor state and nonrevocation immediately before action. A structurally present anchor is insufficient.
3. **Decision enforcement**: a local FFOS effect/read boundary must consume authentic CDX policy outputs, current authority/mandate and Security Twin/revocation facts. It must preserve all seven `CDX-RUNTIME-001` decisions; restrictive outcomes cannot dispatch. E0 classified reads are governed separately from E1-E3 consequential effects; E4 authority mutation has its own approval path.
4. **Evidence and currentness**: policy decision, current facts, controls/obligations and SPETL v1.1 receipts must be independently verified and preserved before consequential completion. Recheck membership, anchor, revocation, facts and policy at the effect boundary. Unknown remote outcome enters hold/reconciliation, not automatic replay.
5. **Fail closed**: missing or invalid host identity, absent registry attestation, excluded/unknown membership, release-pin mismatch, failed anchor verification, policy unavailability, missing mandatory controls or evidence unavailability prevents action.
6. **Independent validation**: conduct adversarial negative cases, real authenticated host/registry/policy/receipt test, independent evidence custody and live effect mediation review. Synthetic provider tests are engineering evidence, not `VERIFIED_RUNTIME_BOUND`.
7. **Approval and scope**: only human-authorized, repository-local integrations may change anchor/runtime standing. CDX is the canonical governance publisher, not a universal superadministrator. A single verified consumer does not prove Estate-wide enforcement.

## Engineering activity in this session

A candidate FFOS host-attested Estate admission module and eight local negative/positive regression tests were authored and executed with Node 22 (8/8 pass). **The GitHub write for that module was blocked by tool safety controls; the candidate therefore remains a local artifact, not committed, connected, deployed or certified.** This source status must be preserved in all downstream summaries. No host credential service, authentic signed registry feed, live policy engine, custody service, protected branch rule or production execution setting was changed.

## Next independent gates

| Gate | Currently observed |
| --- | --- |
| CDX released policy and verified Estate repository anchors (WP10) | PASS 28/28 |
| FFOS host-attested registry membership at admission and effect time | CANDIDATE LOCAL TESTS / NOT COMMITTED |
| FFOS authentic release/anchor verifier and current revocation | NOT VERIFIED LIVE |
| FFOS signed policy evaluation and complete mandatory controls | NOT VERIFIED LIVE |
| FFOS SPETL consumer custody and reconciliation | NOT VERIFIED LIVE |
| FFOS actual effect/read mediation and independent test | NOT VERIFIED LIVE |
| Human approval for runtime standing | NOT YET REQUESTED |

**Disposition:** WP11 remains `BOUND_PENDING_RUNTIME_INTEGRATION`. Neither CDX `enforcement_state` nor FFOS `CDX_RUNTIME_VERIFIED` may be promoted on this evidence.

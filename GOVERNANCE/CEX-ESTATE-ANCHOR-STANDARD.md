# CEX Estate Anchor Standard

**Standard ID:** `CEX-GOV-ANCHOR-001`  
**Canonical authority:** Conductellence (`CEX`)  
**Status:** foundational estate-governance standard  
**Scope:** every repository, runtime or governed work surface admitted to the Conductellence estate

## 1. Canonical rule

Every governed work surface shall maintain a **local technical anchor to CEX**.

The estate relationship is:

```text
CEX  ──publishes governance──>  ALL GOVERNED WORK
CEX  <──local anchor / hook───  ALL GOVERNED WORK
```

This is an asymmetrical bidirectional governance relationship.

- **CEX → work:** constitutional law, signed/versioned policy, control contracts, required schemas, revocations and conformance requirements are published outward from CEX.
- **work → CEX:** every governed work surface carries a machine-readable local anchor identifying the CEX authority, the pinned governance version, the local enforcement surface and the evidence/conformance relationship.

## 2. Why this direction is canonical

CEX shall not use central write-access into every governed repository as its normal governance mechanism. That design creates unnecessary blast radius, couples constitutional authority to downstream repository administration and makes local ownership ambiguous.

Instead:

1. CEX owns and publishes the governing contract.
2. Each governed repository owns its local enforcement point.
3. Each repository binds itself to a defined CEX version through a standard anchor.
4. CEX independently records the governed surface in the estate registry and verifies conformance.
5. Drift, missing anchors, stale policy pins or failed verification may degrade or revoke governance-bound status.

Central publication and local binding are therefore both required. Neither alone is sufficient.

## 3. Mandatory local anchor

The canonical repository location is:

```text
.cex/anchor.json
```

A governed repository without this file, or an equivalent formally registered adapter, is not `CEX_BOUND`.

The anchor shall identify at minimum:

- anchor schema/version;
- governed system/repository identity;
- canonical CEX authority repository;
- CEX law ID and governance/policy version;
- binding mode and policy pin;
- local enforcement point(s);
- authority and mandate context requirements;
- conformance/audit surface;
- SPETL/evidence relationship where applicable;
- current binding state;
- last verification metadata.

The canonical schema is [`../DISTRIBUTION/cex-anchor.schema.json`](../DISTRIBUTION/cex-anchor.schema.json).

## 4. Binding modes

A local anchor shall declare one of:

- `PINNED_RELEASE` — required for production/consequential runtime enforcement; binds to an immutable CEX release/policy digest.
- `PINNED_COMMIT` — permitted for controlled development or pre-release integration.
- `TRACKING` — permitted only for non-consequential development/reference surfaces; must not be represented as production enforcement.

Production effects shall not depend on an unpinned moving governance target.

## 5. Anchor states

The canonical binding states are:

- `UNBOUND` — no valid CEX anchor.
- `ANCHOR_DECLARED` — anchor exists but has not passed verification.
- `CEX_BOUND` — anchor identity and policy pin verified.
- `CEX_CI_MONITORED` — binding plus automated conformance checks.
- `CEX_RUNTIME_GUARDED` — local runtime guard exists but full consequential mediation is not yet verified.
- `CEX_RUNTIME_VERIFIED` — consequential local enforcement has been verified with required evidence.
- `CEX_DEGRADED` — anchor exists but drift, stale policy, unavailable evidence or failed conformance prevents full standing.
- `CEX_REVOKED` — CEX authority or local human authority has explicitly revoked the binding.

These anchor states complement, and do not replace, the runtime integration states defined by `CDX-RUNTIME-001`.

## 6. Local enforcement rule

The anchor does not make CEX a universal super-admin.

```text
CEX defines the governing contract.
The governed system owns the local enforcement point.
```

For consequential action, the local system must be able to demonstrate:

```text
intent
→ identity / authority / mandate
→ pinned CEX governance context
→ policy decision
→ restrictive result where required
→ evidence
→ permitted effect only
→ reconciliation
```

## 7. Push semantics

Within Conductellence architecture, **push** means governed publication/distribution from CEX, not unrestricted direct mutation of downstream repositories.

Canonical CEX publication may include:

- signed or immutable release artifacts;
- policy bundles and shards;
- schemas and control contracts;
- revocation/suspension state;
- audit/conformance requirements;
- compatibility declarations.

A downstream repository consumes and pins those artifacts through its local anchor.

Direct CEX-authored changes to downstream repositories may occur only through a separately authorised maintenance/deployment mechanism and must not be confused with the constitutional governance relationship itself.

## 8. Dual registration rule

A governed work surface shall be represented in two places:

```text
CEX estate registry  <──central discovery / status
        AND
local .cex/anchor.json <──binding / enforcement declaration
```

The estate registry prevents orphaned governed systems. The local anchor prevents false central claims of governance over a repository that has not actually bound itself to CEX.

## 9. Admission rule for new repositories

No new repository intended to belong to the governed estate should be considered governance-ready until the CEX anchor is installed at repository creation or admission.

Recommended creation sequence:

```text
repository created
→ .cex/anchor.json installed
→ CEX identity/policy pin declared
→ estate registry entry created
→ CI conformance hook installed
→ runtime adapter added where consequential execution exists
→ verification state advanced
```

## 10. Existing repositories

Existing estate repositories shall migrate from legacy Conductellence bindings to the canonical `.cex/anchor.json` form without destroying working historical integration evidence.

Legacy `.security/conductellence.json`, local policy copies and existing binding workflows may remain during migration, but the CEX anchor becomes the canonical top-level binding declaration.

## 11. Failure rule

For governed consequential execution:

- missing anchor;
- invalid anchor;
- unknown CEX authority;
- unresolved policy pin;
- revoked binding;
- failed mandatory conformance;

shall never silently degrade to unrestricted execution.

The applicable local enforcement point must fail closed, restrict the effect, or enter explicit human review according to the governing policy.

## 12. Governing maxim

> **CEX governs outward; every governed system anchors inward.**

Or in estate shorthand:

```text
CEX > governance published to > ALL WORK
ALL WORK > technically anchored to > CEX
```

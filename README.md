# Conductellence

**Canonical short name:** `CDX`  
**Name derivation:** **Code of Conduct + Excellence**  
**Canonical system:** `CDX-SYS-001`  
**Canonical law:** `CDX-LAW-001`  
**Current law version:** `1.0.0`  
**Current CDX release:** `1.0.0` — `RELEASED`

> `CDX` is the sole canonical short name for Conductellence in architecture, governance, identifiers and integration language. No parallel system shorthand is permitted.

## Current system state

Conductellence state is represented on independent axes rather than by one overloaded label.

- **Constitutional state:** `ADOPTED`
- **Core runtime state:** `VERIFIED_REFERENCE_RUNTIME`
- **Release state:** `RELEASED`
- **Enforcement state:** `BOOTSTRAP`
- **Estate integration state:** `PENDING_RUNTIME_BINDINGS`

Canonical machine-readable state is held in [`GOVERNANCE/system-state.json`](GOVERNANCE/system-state.json). State semantics are defined in [`GOVERNANCE/state-model.md`](GOVERNANCE/state-model.md).

**Maturity is not enforcement. Release is not integration. Integration is not estate-wide enforcement.**

## CDX 1.0 closure boundary

The CDX 1.0 core is **released**. [`CDX-RC01-BOUNDARY-001`](GOVERNANCE/release-boundary-v1.json) preserves the frozen 1.0 core topology and keeps core release separate from estate execution. WP00–WP09 are complete; WP10–WP14 cover independent anchor verification, first runtime bindings, Pius verification, FFC admission and estate-wide propagation.

Conductellence is the root constitutional, security, legal-governance, assurance and traceability authority for governed non-human digital operation across the estate.

It is deliberately **not** a universal super-admin. Its governing model is:

> **CDX publishes constitutional authority and signed/versioned policy outward; every governed work surface maintains a local technical anchor back to CDX.**

The canonical estate direction is therefore:

```text
CDX  ──publishes/pushes governance──>  ALL GOVERNED WORK
CDX  <────local anchor / hook────────  ALL GOVERNED WORK
```

This is an **asymmetrical bidirectional governance model**:

- CDX is the source of constitutional law, policy contracts, governance versions and conformance requirements.
- Governed repositories own their local enforcement points and must carry an explicit CDX anchor.
- CDX does not normally mutate downstream repositories directly. It publishes governance artifacts; repositories bind to an explicit version and prove conformance.
- Every governed repository must be discoverable from the CDX estate registry, but registry membership does not replace the local anchor.
- A repository without a valid CDX anchor is not considered governance-bound, even if it is listed centrally.

The normative specification is [`GOVERNANCE/CDX-ESTATE-ANCHOR-STANDARD.md`](GOVERNANCE/CDX-ESTATE-ANCHOR-STANDARD.md).

Human sovereign authority remains superior. Conductellence governs the boundary at which human authority is delegated into non-human execution.

## Law-first architecture

Development proceeds from law downward:

1. [**LAW**](LAW/CONDUCTELLENCE-ACT.md) — normative internal constitutional source.
2. [**INTERPRETATION**](INTERPRETATION/INTERPRETATION-GUIDE.md) — structured interpretation, edge cases, precedent and explanations.
3. **CONTROL-CATALOGUE** — machine-addressable § → control → audit bindings.
4. **POLICY** — policy-as-code implementing controls.
5. **AUDITS** — automated tests bound to Chapters and §§.
6. **SPETL** — execution, boundary, decision, incident and assurance evidence.
7. **SECURITY-TWIN** — current/historical reachability, authority and blast radius.
8. **APPENDICES** — HCC, Ex-Inerta Libertad and the Global Authority Corpus.

The Pius provenance and governance relationship between HCC, Ex-Inerta Libertad and the Piusite agent framework is preserved in [`appendices/PIUS-GOVERNANCE-LINEAGE.md`](appendices/PIUS-GOVERNANCE-LINEAGE.md). HCC and Ex-Inerta are source-linked doctrines with different functions and must not be flattened into a single generic AI-governance concept.

The repository therefore follows:

```text
global knowledge / law / standards / research
                    ↓
          Conductellence Act
                    ↓
            Chapter + §
                    ↓
          Interpretation Guide
                    ↓
               Control
                    ↓
          Policy / Protocol
                    ↓
          Enforcement Point
                    ↓
                Audit
                    ↓
            SPETL Evidence
                    ↓
     Security Twin / Meta-Audit
```

## Foundational doctrine

Conductellence preserves the chain:

```text
human mandate
→ authority
→ principal
→ capability
→ information
→ model/tool
→ execution
→ boundary crossing
→ state change
→ external effect
→ evidence
→ responsibility
```

## Drafting discipline

Conductellence is intended to be **all-encompassing by coverage, not by artificial multiplication of clauses**.

The Act contains a dense constitutional rule set. The Interpretation Guide, control catalogue, protocols, test library and Global Authority Corpus are expected to become much larger than the Act. New §§ are added only where they establish a distinct duty, prohibition, permission, presumption, definition, exception or interpretive rule.

## Status notice

Conductellence is an **internal constitutional and control system**, not legislation enacted by a state and not a substitute for qualified legal advice. Applicable external law and fundamental rights remain superior wherever they apply.

The adopted constitutional law is authoritative for governed Conductellence development. Constitutional adoption does not itself establish technical enforcement: a provision is represented as technically enforced only when its mapped controls, runtime gates and evidence requirements have passed their defined acceptance criteria.

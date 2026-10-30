# CDX 1.0 System Guide

## Purpose

This guide explains Conductellence as an operating governance system rather than as a development programme.

CDX exists to make non-human digital execution answerable to explicit human authority, bounded mandate, verifiable policy and durable evidence.

## 1. Mental model

Think of CDX as five connected systems:

~~~text
1. Constitution        What is allowed, required or prohibited?
2. Authority model     Who may authorize whom to do what?
3. Runtime control     May this specific action happen now?
4. Evidence system     What proves the decision and resulting effect?
5. Estate governance   Which systems are bound, and at what maturity?
~~~

None of these layers substitutes for another.

## 2. Constitutional layer

The canonical normative source is CDX-LAW-001.

The law defines duties, prohibitions, permissions, presumptions, definitions, exceptions and interpretive rules. Implementation stays below the law:

~~~text
Law
→ Interpretation
→ Control
→ Policy
→ Enforcement point
→ Audit
→ Evidence
~~~

This prevents policy implementation from silently redefining constitutional meaning.

## 3. Authority model

The central invariant is:

> **Identity does not grant authority.**

A runtime request must be attributable to a principal and, where consequential, must carry explicit authority and mandate references.

CDX separates:

- principal identity;
- human authority;
- mandate;
- delegated capability;
- workflow scope;
- runtime effect class;
- evidence;
- acceptance.

A model can produce content or reasoning, but model identity does not automatically become the accountable principal.

## 4. Runtime contract

CDX-RUNTIME-001 defines the consumer contract.

A consumer runtime resolves the operating surface, principal, action, authority reference, mandate reference, effect, target, run identity, current trust state and pinned policy context.

The seven outcomes are:

- ALLOW
- ALLOW_WITH_CONTROLS
- REQUIRE_HUMAN
- QUARANTINE
- DENY
- SECURITY_STOP
- CONSTITUTIONAL_STOP

The vocabulary distinguishes ordinary denial from unavailable trust infrastructure and from constitutional prohibition.

## 5. Fail-closed runtime

Missing governance never becomes permission.

Examples include:

- policy unavailable;
- policy parse/integrity failure;
- unknown policy operation;
- no applicable control;
- invalid or revoked anchor;
- required evidence unavailable;
- absent authority or mandate.

## 6. Effect mediation

A consequential effect is not authorized merely because a policy function once returned ALLOW.

~~~text
resolve current authority
→ validate local anchor
→ evaluate pinned policy
→ write PRE_EFFECT evidence
→ re-check currentness / revocation
→ execute local effect
→ write POST_EFFECT evidence
→ independent verification / reconciliation where required
~~~

If an external callback fails after dispatch, the outcome is uncertain and must be reconciled. Blind automatic replay is not accepted.

## 7. SPETL evidence

SPETL is the canonical execution/evidence layer.

An event binds actor, action, authority, mandate, policy, decision, control results, effect status, run/correlation identifiers and evidence references into a reconstructable chain.

Evidence authority is separately governed so the executing actor cannot simply certify itself.

## 8. Security Twin

The Security Twin provides the structural context around execution:

- authority relationships;
- dependencies;
- reachability;
- trust domains;
- assets;
- potential blast radius;
- historical state where required.

Runtime policy can therefore be evaluated against system context rather than an isolated model prompt.

## 9. Estate governance

CDX applicability is determined by the Estate Registry.

A repository can be:

- authority source;
- governed applicable;
- excluded by explicit decision;
- historical alias.

GitHub organization membership does not determine this classification.

### Repository anchor

The local .cdx/anchor.json binds a governed repository to CDX and records its identity, CDX authority, law, release/policy pin, local enforcement ownership, conformance state, evidence expectations and verification state.

### Anchor versus runtime

CDX_BOUND / PASS proves repository governance binding.

It does not prove that the application mediates consequential effects.

Runtime standing requires effect-level evidence.

## 10. Independent state axes

CDX avoids one overloaded “done” flag.

### Constitutional
FOUNDATIONAL_DRAFT → CONSTITUTIONAL_CANDIDATE → STABLE_CANDIDATE → ADOPTED → AMENDED

### Core runtime
SPECIFIED → IMPLEMENTED → TESTED → VERIFIED_REFERENCE_RUNTIME → PRODUCTION_REFERENCE

### Release
DEVELOPMENT → PRE_RELEASE → RELEASED → SUPERSEDED → RETIRED

### Enforcement
NON_ENFORCING → BOOTSTRAP → ENFORCEMENT_READY → ENFORCING → SUSPENDED

### Estate integration
NOT_STARTED → PENDING_RUNTIME_BINDINGS → CONTRACT_AVAILABLE → BINDINGS_IN_PROGRESS → PARTIALLY_BOUND → VERIFIED_RUNTIME_BOUND

A move on one axis never silently moves the others.

## 11. Controls and review-governed law

Not every constitutional rule should become a machine predicate.

CDX separates implemented reference controls from review-governed provisions requiring human or structured review. This prevents false precision and preserves judgment where automated policy would be inappropriate.

## 12. Legal and regulatory resolution

External law is source-bound, not copied into CDX as timeless truth.

Legal references and regulatory drift mechanisms track authoritative source changes. A changed or unresolved source cannot silently become a new operational interpretation.

## 13. Assurance chain

CDX assurance combines:

- constitutional integrity;
- exact legal-reference integrity;
- law-to-control coverage;
- review governance;
- runtime distribution tests;
- SPETL integrity;
- independent evidence preservation/custody;
- Security Twin checks;
- estate reconciliation;
- adversarial acceptance;
- enforcement-transition tests;
- human sovereign approval.

This is why “implemented,” “tested,” “reference verified,” “runtime bound” and “enforcing” are separate claims.

## 14. Example: governed repository effect

~~~text
Automation requests an E2 repository change
→ host resolves active identity/workflow/capability
→ target is checked against mandate
→ local CDX anchor is current
→ authority_ref + mandate_ref are resolved
→ pinned CDX policy evaluates required surfaces
→ restrictive result: BLOCKED evidence, no repository write
→ permissive result: PRE_EFFECT evidence
→ currentness/revocation rechecked
→ repository change executes
→ POST_EFFECT evidence
→ verifier reconciles result
~~~

The model never gains write authority merely because it knows how to call GitHub.

## 15. Operational roles

### Human / Director
Owns purpose, mandate, approval and acceptance.

### CDX
Publishes constitutional authority, policy contracts, runtime semantics and assurance requirements.

### Governed consumer
Owns the local application and enforcement point.

### Agent / automation
Executes only inside admitted identity, capability, workflow and mandate.

### Verifier / custodian
Independently validates or preserves evidence outside the actor's unilateral control.

## 16. What “finished CDX 1.0” means

CDX 1.0 construction is final-accepted.

The canonical governance system, stable release, estate registry, anchor propagation, reference runtime, evidence architecture and programme assurance are complete.

This does not mean every governed consumer has completed consequential runtime integration. Consumer bindings remain separately evidenced.

## Canonical references

- Law — LAW/CONDUCTELLENCE-ACT.md
- State model — GOVERNANCE/state-model.md
- Machine state — GOVERNANCE/system-state.json
- Runtime contract — RUNTIME-INTEGRATION/CDX-RUNTIME-001.json
- Policy registry — POLICY/control-registry.json
- Estate registry — ESTATE-REGISTRY/registry-v2.json
- Anchor standard — GOVERNANCE/CDX-ESTATE-ANCHOR-STANDARD.md
- SPETL — SPETL/
- Security Twin — SECURITY-TWIN/
- Terminal audit — AUDITS/CDX-1.0-TERMINAL-AUDIT-2026-10-30.md
- End report — PROGRAMME/CDX-1.0-END-REPORT-2026-10-30.md

# CDX-CLR-LEGAL-BD-001 — Clearance and Execution Order for Legal Integrity Phases B–D

**Order ID:** `CDX-CLR-LEGAL-BD-001`  
**Authority class:** HUMAN_SOVEREIGN_EXECUTION_CLEARANCE  
**Issued:** 24 September 2026  
**Applies to:** Conductellence `CDX-SYS-001` / Conductellence Act `CDX-LAW-001`  
**Programme:** Legal Citation & Applicability Integrity  
**Phases authorized:** B → C → D  
**Execution model:** Household Family — Director / Janitor / Handyman  
**Continuity:** CONTINUOUS_WITH_GATES  
**Order state:** ACTIVE

## 1. Human clearance

Human sovereign authority hereby clears Conductellence to proceed continuously through **Phase B — Semantic Support Proof**, **Phase C — Legal Applicability Resolver**, and **Phase D — Regulatory Drift & Temporal Legal State** without requiring a new conversational “proceed” instruction at ordinary work-package or phase boundaries.

This order authorizes work. It does **not** pre-authorize PASS.

Director controls progression. Janitor scans coherence, provenance, security, legal-reference integrity and control contradictions. Handyman may execute only registered deterministic J1 repairs. The Household controller may orchestrate these roles but acquires no additional authority.

## 2. Governing Household sequence

The mandatory control loop for Phases B–D is:

```text
HUMAN CLEARANCE
      ↓
DIRECTOR DISPATCH
      ↓
JANITOR PRE-SCAN
      ↓
IMPLEMENTATION / RESEARCH
      ↓
JANITOR SCAN
      ↓
eligible J1 defect ──→ HANDYMAN bounded repair
      │                         │
      └──────────────← re-scan ┘
      ↓
CI / LEGAL-INTEGRITY AUDITS
      ↓
DIRECTOR ACCEPTANCE OR BLOCK
      ↓
NEXT DEPENDENCY-READY PHASE
```

Director acceptance applies only to the committed state under audit. An ephemeral workspace, draft, generated proposal, chat statement or uncommitted repair cannot become PASS.

## 3. Phase B — Semantic Support Proof

### Objective

Determine, paragraph by paragraph and provision by provision, whether an exact external legal provision:

1. is merely a relevant reference (`CONTEXTUAL`);
2. supports an explicit internal derivation (`DERIVED`); or
3. materially states the same proposition (`TEXTUAL`).

### Mandatory rule

No `DERIVED` or `TEXTUAL` relation may be promoted without an exact semantic proof record identifying:

- Conductellence paragraph ID;
- exact legal provision ID;
- exact official locator;
- primary official source;
- Conductellence proposition;
- conservative external legal proposition;
- reasoning bridge;
- support boundary;
- verification date;
- review state.

### Phase-B hard stops

The following are J2 / human or legal-review matters and may not be auto-repaired:

- ambiguity about the meaning of external law;
- conflicting primary legal texts or authoritative interpretations;
- promotion to `TEXTUAL` where equivalence is disputable;
- a proposed proof that would convert an internal CDX policy choice into a falsely claimed statutory obligation;
- any need to amend the constitutional meaning of `CDX-LAW-001`.

### Phase-B clearance criterion

Director may clear Phase B only where:

- every stronger support claim is bound to a valid proof;
- no unproven `DERIVED` or `TEXTUAL` relation exists;
- proof syntax, source identity and paragraph/provision IDs pass CI;
- unresolved semantic questions are explicitly represented as unresolved rather than guessed.

## 4. Phase C — Legal Applicability Resolver

### Objective

Build the machine-readable resolver that determines whether a verified external legal provision applies to a particular governed system and operation.

Applicability shall be resolved independently from citation relevance and semantic support.

### Minimum applicability dimensions

The resolver shall represent at least:

- jurisdiction;
- territorial nexus;
- legal instrument status;
- effective and transition dates;
- actor role;
- organisation/entity class;
- sector;
- system/AI class;
- provider/deployer/controller/processor or equivalent legal role;
- data categories;
- data-subject location where legally relevant;
- processing/action purpose;
- external effect;
- contractual overlay;
- statutory exemption/carve-out;
- national implementation relationship;
- unresolved legal facts.

### Result grammar

At minimum:

`APPLIES · DOES_NOT_APPLY · PARTIALLY_APPLIES · CONDITIONAL · UNKNOWN · LEGAL_REVIEW_REQUIRED`

`UNKNOWN` shall never silently become `DOES_NOT_APPLY`.

### Phase-C hard stops

Handyman may not mechanically decide:

- disputed jurisdiction;
- materially ambiguous actor classification;
- conflicts of laws;
- statutory exemptions requiring legal interpretation;
- whether a novel AI/agent arrangement falls within a contested legal category.

### Phase-C clearance criterion

Director may clear Phase C only where:

- every applicability result identifies the exact facts and legal records on which it depends;
- missing facts propagate as UNKNOWN or LEGAL_REVIEW_REQUIRED;
- citation presence cannot itself create APPLIES;
- historic decisions can be reconstructed against the legal snapshot and system facts used at the time.

## 5. Phase D — Regulatory Drift & Temporal Legal State

### Objective

Continuously detect and govern changes in the external legal material on which Conductellence relies.

### Mandatory tracked changes

The drift system shall be able to represent:

- publication;
- entry into force;
- application date;
- transition period;
- amendment;
- corrigendum;
- repeal;
- supersession;
- national implementation;
- delegated/implementing act;
- official guidance relevant to interpretation;
- authoritative judicial or regulatory interpretation where admitted to the corpus;
- source relocation;
- source retrieval failure;
- verification staleness.

### Drift rule

A source change shall not automatically rewrite historic legal state.

Conductellence shall preserve:

```text
LEGAL SNAPSHOT AT EXECUTION
            +
CURRENT LEGAL STATE
            +
CHANGE EVENT / SUPERSESSION PATH
```

### Phase-D hard stops

Automatic drift processes may detect, fetch, hash, compare, classify obvious metadata changes and create findings. They may not autonomously:

- decide the substantive legal effect of an ambiguous amendment;
- declare a law inapplicable because a source URL failed;
- overwrite historic legal evidence;
- silently change a `DERIVED` or `TEXTUAL` support proof;
- expand agent authority because an external law changed.

### Phase-D clearance criterion

Director may clear Phase D only where:

- drift events are append-oriented and attributable;
- current and historic legal state remain distinguishable;
- verification freshness is measurable;
- source failures produce findings rather than invented legal state;
- substantive changes trigger re-evaluation of affected support proofs, applicability decisions and controls.

## 6. Clearance boundaries

This Order authorizes:

- source verification;
- primary-law retrieval;
- machine-readable legal registries;
- semantic proof drafting;
- applicability schemas and deterministic resolution logic;
- legal-state snapshots;
- regulatory-drift detectors;
- registered J1 repairs;
- CI/audit scripts;
- branch/PR work;
- Director progression through B–D when gates pass.

This Order does **not** authorize:

- autonomous constitutional amendment;
- autonomous legal advice or adjudication;
- invention of legal propositions;
- unsupported article/§ references;
- promotion of uncertain law to authoritative fact;
- bypass of legal-review requirements;
- silent conversion of J2 findings into J1 repairs;
- lowering an existing security or legal control to obtain PASS;
- treating an AI/model output as a legal source.

## 7. Repair classes for this programme

- **J0** — ephemeral formatting/cache/output cleanup; no legal-state mutation.
- **J1** — deterministic registered repair whose correct result follows mechanically from authoritative committed inputs.
- **J2** — legal interpretation, constitutional meaning, authority change, disputed source meaning, disputed applicability, or any repair requiring substantive judgment.

Examples of valid J1 repair:

- correcting a paragraph-map ID to match the canonical section ID where both are explicit;
- replacing a stale copied locator with the already-verified canonical locator from the registry;
- regenerating a deterministic index from accepted source records.

Examples of J2:

- deciding that an AI Act article applies to a novel agent architecture;
- deciding that two legal propositions are semantically equivalent;
- deciding that a statutory exemption applies;
- deciding that an amendment changes the constitutional meaning of Conductellence.

## 8. Continuous progression rule

Once this Order is committed and passes constitutional CI:

1. Phase B is `DISPATCHED`.
2. Phase C is `CLEARED_PENDING_B`.
3. Phase D is `CLEARED_PENDING_C`.
4. Director may dispatch the next phase automatically when the preceding phase has a committed PASS and no inherited hard stop.
5. No additional conversational proceed instruction is required.
6. A `SECURITY_STOP`, `CONSTITUTIONAL_STOP`, unresolved `LEGAL_REVIEW_REQUIRED`, or explicit human hold suspends progression.

## 9. Audit authority statement

The following statement is the canonical reference language for audits, acceptance records, pull requests and phase closeout reports:

> **Audit authority — CDX-CLR-LEGAL-BD-001:** Human sovereign authority cleared continuous execution of Conductellence Legal Integrity Phases B–D under Household Family control. The clearance authorizes research, exact-source verification, semantic-proof work, applicability-engine development, temporal legal-state and regulatory-drift infrastructure, registered deterministic J1 repair, CI and sequential Director dispatch. It does not pre-authorize PASS, legal applicability judgments, disputed semantic equivalence, constitutional amendment, bypass of hard stops, or autonomous expansion of authority. Director acceptance is valid only for committed state under audit after required Janitor scan, permitted repair, re-scan and phase-specific acceptance gates.

### Compact machine/audit citation

`AUTHORITY_REF=CDX-CLR-LEGAL-BD-001`

### Required audit fields

Every Phase B–D audit/acceptance record shall include:

```text
authority_ref: CDX-CLR-LEGAL-BD-001
phase: B | C | D
director_state:
janitor_scan_ref:
handyman_repair_refs:
ci_run_ref:
committed_sha:
hard_stops:
unresolved_legal_review:
acceptance_state:
accepted_at:
```

## 10. Order precedence and expiry

This Order governs execution sequencing for Phases B–D. It does not supersede `CDX-LAW-001`, applicable external law, or a later explicit human order.

The Order expires for new execution when Phase D is formally closed, revoked by human authority, or superseded by a later clearance order. Its audit authority reference remains historically valid for work performed under it.

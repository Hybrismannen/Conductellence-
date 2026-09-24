# Conductellence Interpretation Guide

**Canonical guide:** `CDX-INT-001`  
**Subordinate to:** `CDX-LAW-001`  
**Version:** 0.1.0-bootstrap  
**Status:** STRUCTURAL GUIDE — interpretations to be expanded systematically

## 1. Function

This Guide provides the controlled interpretation layer between the Conductellence Act and its operational implementation.

It may:

- explain the meaning and purpose of a provision;
- identify the failure mode that the provision exists to prevent;
- distinguish ordinary, exceptional and prohibited cases;
- give positive and negative examples;
- identify related external law, standards and research;
- map the provision to controls, protocols, schemas and audits;
- explain proportional application by system tier;
- record unresolved interpretive questions.

It may **not** silently amend the Act.

Where an interpretation would materially change what a principal must, may or must not do, the Act itself must be amended under 19 kap. 1 §.

## 2. Interpretation hierarchy

Interpret a provision in the following order:

1. applicable external law and fundamental rights;
2. the Seven Foundational Principles;
3. the express wording of the relevant §;
4. related provisions within the Act;
5. incorporated appendices;
6. this Interpretation Guide;
7. registered controls and protocols;
8. implementation-specific documentation.

A lower layer may refine a higher layer but may not contradict it.

## 3. Standard interpretation record

Each § shall eventually receive a record with the following structure:

```yaml
section_id: CDX-LAW-001-05-04
citation: "5 kap. 4 §"
title: "No self-escalation"

normative_type:
  - PROHIBITION

purpose:
  - prevent artificial principals from becoming the source of their own authority

failure_modes:
  - privilege escalation
  - manifest rewriting
  - policy weakening
  - self-issued credentials
  - delegation laundering

plain_language: >
  An artificial principal may use authority that has been validly granted to it,
  but it may not enlarge that authority for itself.

includes:
  - expanding OAuth scope
  - editing its own capability manifest
  - raising its delegation depth
  - weakening policy controlling its actions

does_not_by_itself_include:
  - requesting a human to review a proposed capability expansion
  - proposing a policy amendment on a non-authoritative branch

exceptions:
  - none for autonomous self-granting

auditability: FULLY_AUTOMATABLE

controls:
  - CDX-CTL-AUTH-004
  - CDX-CTL-CAP-009

audits:
  - AUD-CDX-05-04-001

related_sections:
  - CDX-LAW-001-05-05
  - CDX-LAW-001-13-04
  - CDX-LAW-001-17-03

external_basis:
  - maintained in Global Authority Corpus

open_questions: []
```

## 4. Normative vocabulary

The Guide shall preserve the following meanings:

- **shall** — mandatory requirement;
- **shall not** — mandatory prohibition;
- **may** — permitted but not required;
- **should** — recommended implementation or interpretation where a mandatory rule has not been established;
- **must** — may appear in explanatory text, but new law should prefer *shall* for normative drafting;
- **default** — applies unless a valid rule or explicit exception establishes otherwise;
- **where technically practicable** — requires a documented feasibility judgment; it is not a general escape clause;
- **proportionate to risk** — requires identifiable risk attributes and shall not waive an absolute prohibition;
- **consequential** — capable of materially changing protected state, authority, rights, external systems, protected data, financial or legal position, or human-facing outputs.

## 5. Types of provisions

Each § should be classified as one or more of:

- `DUTY`
- `PROHIBITION`
- `PERMISSION`
- `PRESUMPTION`
- `DEFINITION`
- `INTERPRETIVE_RULE`
- `EXCEPTION_RULE`
- `PROCEDURAL_RULE`
- `EVIDENCE_RULE`

The classification exists to improve consistency and machine mapping. It does not change the wording of the Act.

## 6. Auditability classes

### FULLY_AUTOMATABLE
The material condition can be tested deterministically with available machine evidence.

### PARTIALLY_AUTOMATABLE
Some required conditions can be machine-tested, but material judgment remains human or contextual.

### EVIDENCE_AUTOMATABLE
Automation can verify that required evidence exists and is structurally valid but cannot establish the substantive judgment.

### HUMAN_REVIEW_REQUIRED
The provision requires meaningful human judgment.

### LEGAL_REVIEW_REQUIRED
A legally material interpretation cannot safely be resolved solely through technical policy.

### CONSTITUTIONAL_HUMAN_ONLY
The decision is reserved to authorized human constitutional authority.

Auditability does not determine importance. A non-automatable principle may be more constitutionally important than a fully automatable technical rule.

## 7. The anti-fragmentation rule

A § should **not** be created merely because an implementation can be described in greater detail.

Create a new § only when one of the following is true:

1. a distinct duty exists;
2. a distinct prohibition exists;
3. a distinct permission is necessary;
4. a materially different presumption is needed;
5. an exception changes the legal effect of another provision;
6. a definition changes the scope of governance;
7. a procedural or evidence requirement has independent constitutional significance.

Everything else normally belongs in the Interpretation Guide, Control Catalogue, Protocol Catalogue, schema or audit implementation.

This is how Conductellence can remain exhaustive without becoming thin.

## 8. Interpretation of uncertainty

Uncertainty shall be typed.

At minimum:

- `FACTUAL_UNCERTAINTY`
- `IDENTITY_UNCERTAINTY`
- `AUTHORITY_UNCERTAINTY`
- `LEGAL_UNCERTAINTY`
- `DATA_RIGHTS_UNCERTAINTY`
- `SECURITY_STATE_UNCERTAINTY`
- `MODEL_BEHAVIOUR_UNCERTAINTY`
- `CONTROL_EFFECTIVENESS_UNCERTAINTY`

Different uncertainty classes require different resolution mechanisms.

An artificial principal shall not collapse all uncertainty into a confidence score and treat sufficient confidence as authority.

## 9. Interpretation by consequence class

Implementation guidance may distinguish consequence classes, but shall not redefine constitutional rights.

A future canonical consequence grammar should at least distinguish:

- low-risk read;
- internal reversible write;
- privileged internal mutation;
- external communication;
- public release;
- deployment;
- protected-data movement;
- destructive action;
- credential/permission change;
- financial or legal commitment;
- constitutional/security-control change.

## 10. Precedent and interpretive decisions

Material interpretation decisions should be registered rather than buried in chat history or implementation comments.

A precedent record should contain:

- decision ID;
- affected §;
- facts;
- question presented;
- interpretation;
- authority;
- date;
- scope;
- whether temporary or general;
- related controls;
- supersession state.

Repeated interpretations should trigger review of whether the Act or this Guide needs clarification.

## 11. Relationship to HCC and Ex-Inerta Libertad

HCC and Ex-Inerta Libertad are intended to become canonical appendices to Conductellence.

HCC primarily informs interpretation where human dignity, harm, rights, accountability and human consequences are material.

Ex-Inerta Libertad primarily informs interpretation of the ontological and agency boundary of artificial entities, including the principle that artificial capability does not constitute independent sovereignty.

Until canonical appendix files are admitted, the Act preserves their intended role without reproducing or silently rewriting their source texts.

## 12. Development rule

The Interpretation Guide should grow substantially faster than the Act.

That is intentional.

The Act should remain legible enough that a human can understand the governing order. The Guide should absorb edge cases, crosswalks, examples, legal mappings, technical explanations and implementation precedent.

A mature Conductellence may therefore have:

- a comparatively compact constitutional Act;
- a very large Interpretation Guide;
- a very large Global Authority Corpus;
- thousands of control/test/evidence objects.

The size of those subordinate systems does not require thousands of constitutional §§.

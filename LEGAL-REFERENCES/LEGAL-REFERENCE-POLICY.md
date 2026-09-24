# Legal Reference Policy

**Canonical policy:** `CDX-LEGAL-REF-001`  
**Applies to:** `CDX-LAW-001`  
**Status:** strict exact-provision mode

## 1. Non-negotiable rule

Every substantive paragraph in the Conductellence Act shall carry one or more links to **exact provisions in real legal instruments using official primary sources**.

The existence of a citation means only that the identified provision is an exact, verified legal reference associated with that paragraph. It does **not** by itself mean:

- that the external provision legally applies to every Conductellence-governed system;
- that the external provision states the same proposition as Conductellence;
- that the external provision requires Conductellence's technical mechanism;
- that Conductellence may present its internal rule as externally mandated.

These are separate questions and shall remain separately represented.

## 2. Three independent states

Every legal mapping shall distinguish:

1. **Provision existence/locator** — Is the cited legal provision real, exactly located and verified against an official primary text?
2. **Support relationship** — Does that exact provision merely provide context, materially support a derived rule, or textually express the same proposition?
3. **Applicability** — Does that external legal provision actually apply to this system, actor, purpose, jurisdiction and date?

No state may be inferred from another.

## 3. Exact locator syntax

Act citations shall use a registered provision ID linked to exactly one locator, such as:

- `GDPR-32-1-D · Article 32(1)(d)`
- `NIS2-21-2-F · Article 21(2)(f)`
- `SE-CYBER-2-3-6 · 2 kap. 3 § second paragraph point 6`

The following are prohibited in operative Act citations:

- whole-instrument references when a specific provision is being claimed;
- article ranges such as `Articles 12–15`;
- chapter ranges or `§§` ranges;
- vague labels such as “incident provisions”, “governance provisions”, “lifecycle duties” or “where applicable” used as locators;
- citation text generated from memory without a registered exact provision record.

## 4. Reference-only default

The default relationship in the Act is:

`CONTEXTUAL`

Visible Act wording shall state:

> **Exact legal provisions — reference only; support and applicability not asserted:**

This is intentionally conservative.

A contextual citation says only that the exact provision is legally relevant enough to remain attached as a source/reference point. It does not assert that the provision proves or mandates the Conductellence paragraph.

## 5. Stronger support claims

A paragraph × provision relationship may be promoted to `DERIVED` or `TEXTUAL` only when a corresponding object exists in:

`LEGAL-REFERENCES/legal-support-proofs.json`

A proof must state at minimum:

- exact paragraph ID;
- exact provision ID;
- exact locator and official URL;
- Conductellence proposition being assessed;
- conservative paraphrase of the external legal proposition;
- the precise support bridge or textual equivalence;
- the boundary beyond which the external law does not support the Conductellence rule;
- review state and verification date.

### DERIVED

`DERIVED` means the Conductellence rule is a deliberate internal extension or operationalisation of a verified external legal proposition.

The extension must be stated. A derived rule shall never be presented as the literal external-law requirement.

### TEXTUAL

`TEXTUAL` is a high-bar state. It may be used only where the external provision materially expresses the same proposition at the level being claimed.

No `TEXTUAL` relation is permitted during bootstrap unless an explicit semantic proof record passes the legal citation audit.

## 6. Applicability is separate

Legal applicability shall be determined by the future Legal Resolver using system-specific facts including jurisdiction, actor role, sector, purpose, data, location and date.

A paragraph citation must never be treated as an applicability result.

## 7. Primary-source rule

Provision records shall point to official primary legal sources wherever available, including EUR-Lex, Sveriges riksdag/Svensk författningssamling, official treaty repositories or equivalent official national sources.

Technical standards, security frameworks, academic research, regulatory guidance and secondary legal commentary belong in the Global Authority Corpus and Interpretation Guide. They do not satisfy the Act's real-law citation requirement.

## 8. Syntax-level CI enforcement

A constitutional audit shall fail where any of the following occurs:

- a substantive Act paragraph lacks a paragraph ID;
- a § lacks at least one independently cited operative paragraph;
- a cited provision ID is absent from the exact-provision registry;
- a locator differs from the registry;
- a visible URL differs from the official registry URL;
- a generic or ranged citation survives in the Act;
- the Act and paragraph map disagree;
- `DERIVED` or `TEXTUAL` is used without a valid semantic proof;
- a citation is silently treated as an applicability determination.

## 9. Amendment rule

Every future amendment to `CDX-LAW-001` shall satisfy this policy before the constitutional CI gate may pass.

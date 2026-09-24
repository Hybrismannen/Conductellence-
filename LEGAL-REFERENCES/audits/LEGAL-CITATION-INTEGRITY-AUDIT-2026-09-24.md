# Legal Citation Integrity Audit — 2026-09-24

**Audit ID:** `CDX-AUD-LEGAL-2026-09-24-001`  
**Scope:** `CDX-LAW-001` paragraph-level legal references  
**Result:** PASS after remediation  
**CI run:** `36053587879`  
**Verified commit:** `3da676733813e9d4424ae811612b7388fa8f0ce1`

## 1. Audit objective

This audit was initiated because Conductellence requires a higher legal-citation standard than ordinary explanatory writing. A real legal instrument must not be cited in a way that invents an article, misstates a locator, converts a general legal principle into a non-existent precise duty, or implies that a provision applies to a system merely because it is relevant to the architecture.

The audit therefore separates three questions that must never be collapsed:

1. **Existence and locator:** does the cited provision actually exist at the exact stated location in an official primary legal text?
2. **Support:** does that exact provision contextually relate to, support a derivation toward, or textually state the Conductellence proposition?
3. **Applicability:** does the external provision legally apply to the particular governed system, actor, sector, purpose, data, jurisdiction and date?

A citation alone answers none of questions 2 or 3.

## 2. Defects found

### 2.1 Chapter-wide citation bundles

The first legal-reference pass attached repeated chapter-level bundles to many paragraphs. A bundle such as “AI Act Arts. 9 and 14–15” may contain real provisions but does not establish that every provision in the range supports every paragraph to which the bundle is attached.

**Disposition:** removed.

### 2.2 Generic and ranged locators

References such as:

- `Arts. 12–15`;
- “incident/recovery provisions”;
- “lifecycle risk-management obligations”;
- “governance and compliance architecture”;
- generic whole-instrument labels used as if they were pinpoint provisions;

were too imprecise for Conductellence.

**Disposition:** prohibited by CI.

### 2.3 Markdown paragraph-boundary defect

The earlier audit treated some § headings and first operative paragraphs as a single Markdown block. This allowed a § to appear covered even where the first operative proposition had no independent legal-reference identity.

**Disposition:** the Act was normalised line-by-line. Every substantive paragraph now receives its own `cdx:legal` paragraph ID and reference block.

### 2.4 Overstated support classifications

A first semantic pass classified six relationships as `TEXTUAL`. Review showed that the Conductellence propositions extended beyond the wording of those provisions.

**Disposition:** all six were downgraded. The authoritative Act currently contains **zero TEXTUAL claims**.

Further sampling found multiple `DERIVED` mappings that were plausible but broader than the exact source proposition—for example:

- internal identity/authority architecture derived from general access-control provisions;
- crypto-agility and post-quantum migration derived from provisions requiring cryptography;
- internal control architecture derived from provisions requiring assessment of security-measure effectiveness.

The external provisions were real; the asserted derivation was still too strong to leave unqualified.

**Disposition:** all Act mappings were reset to `CONTEXTUAL`.

## 3. Current exact-citation state

At the verified commit:

- **19 Chapters**
- **7 Foundational Principles**
- **131 §§**
- **217 independently addressable substantive paragraphs**
- **217/217 paragraphs carry exact legal-reference metadata**
- **131/131 §§ contain at least one independently cited operative paragraph**
- **88 exact legal provisions are registered as primary-text verified**
- **52 of those exact provisions are currently used in the Act**
- **934 paragraph-to-provision reference edges exist**
- **934/934 are currently `CONTEXTUAL`**
- **0 `DERIVED` claims**
- **0 `TEXTUAL` claims**
- **0 applicability claims derived from citation presence**

## 4. Canonical legal-reference syntax

Each substantive paragraph is followed by a machine marker:

```html
<!-- cdx:legal
     paragraph="CDX-LAW-001-XX-YY-PZZ"
     refs="PROVISION-ID:CONTEXTUAL;..."
     verified="2026-09-24" -->
```

and an immediate human-readable source line:

```markdown
> **Exact legal provisions — reference only; support and applicability not asserted:**
> [PROVISION-ID · exact locator · CONTEXTUAL](official primary-source URL)
```

The visible locator and URL must exactly match the registered provision object.

## 5. Exact-provision registry

`LEGAL-REFERENCES/legal-provision-registry.json` is now the only permitted source for Act provision IDs.

Each provision record includes:

- stable Conductellence provision ID;
- legal instrument;
- exact article/paragraph/point or Swedish chapter/section/point locator;
- official primary-source URL;
- verification date;
- `VERIFIED_PRIMARY_TEXT` state;
- a conservative subject paraphrase.

The current exact registry covers verified provisions from:

- Charter of Fundamental Rights of the European Union;
- Regulation (EU) 2024/1689 — AI Act;
- Regulation (EU) 2016/679 — GDPR;
- Directive (EU) 2022/2555 — NIS2;
- Cybersäkerhetslag (2025:1506).

Broader instruments previously mentioned in conceptual research are **not** promoted to exact Act citations until the relevant provision has been separately verified and registered.

## 6. Semantic support proof

`LEGAL-REFERENCES/legal-support-proofs.json` establishes the next legal quality gate.

A citation may be promoted from reference-only `CONTEXTUAL` to `DERIVED` or `TEXTUAL` only by an explicit paragraph × provision proof record.

The proof must state:

- exact paragraph;
- exact provision;
- exact official locator;
- Conductellence proposition;
- external legal proposition;
- support bridge;
- support boundary;
- verification date;
- review state.

No `DERIVED` or `TEXTUAL` state is currently asserted.

## 7. Applicability

Legal applicability remains intentionally unresolved by the Act citation layer.

A real and accurately cited provision may be:

- relevant to the architecture;
- legally inapplicable to a particular system;
- applicable only to a specific actor role;
- applicable only to personal-data processing;
- applicable only to high-risk AI;
- applicable only to entities within a statutory sector/scope;
- subject to transition dates, national implementation or other conditions.

The future Conductellence Legal Resolver must therefore determine applicability independently from paragraph citation metadata.

## 8. Automated enforcement

`AUDITS/audit_legal_reference_integrity.py` now fails CI if, among other conditions:

1. a registered provision is not marked `VERIFIED_PRIMARY_TEXT`;
2. a locator is empty or uses prohibited vague/range syntax;
3. a substantive § has no independently cited operative paragraph;
4. a paragraph marker references an unknown provision ID;
5. a visible locator differs from the exact registry locator;
6. a visible official URL differs from the registry URL;
7. the Act and paragraph legal map disagree;
8. generic/ranged citation language reappears;
9. a `DERIVED` or `TEXTUAL` relationship lacks an explicit verified semantic proof;
10. support or applicability is inferred merely from reference presence.

## 9. Verified CI result

GitHub Actions run `36053587879` completed successfully.

The exact legal-reference gate reported:

```text
PASS: 131 §§ all have independently cited operative paragraphs
PASS: 217 paragraph legal markers are syntactically exact
PASS: 88 exact provisions are primary-text verified and registered
PASS: Act and paragraph legal map match exactly
PASS: 0 stronger support claims have explicit semantic proofs
PASS: no generic/ranged citation syntax and no unsupported support/applicability claim
```

The remaining constitutional audits also passed:

```text
PASS: 131 §§, 19 chapters, 7 foundational principles
PASS: every § has unique ID and valid auditability class
PASS: every law § is represented in the machine binding registry
PASS: Conductellence canonical root structure present
```

## 10. Residual limitations

This PASS establishes **citation-integrity architecture**, not universal legal correctness.

It proves that:

- legal provision identifiers are exact and registered;
- paragraph/reference syntax is internally consistent;
- broad or invented pinpoint syntax is blocked;
- stronger support claims are not being made without proof.

It does **not** yet prove:

- legal applicability to each governed system;
- that every contextual reference is the best or most complete legal reference for the paragraph;
- that the current registry exhausts all globally relevant law;
- that future amendments to external law have not changed a provision after the recorded verification date.

Those are separate assurance layers to be implemented through semantic proof review, the Global Authority Corpus, the Legal Resolver and regulatory-drift monitoring.

## 11. Governing audit conclusion

The Act is now in a legally conservative citation state:

> **Exact provision existence is asserted only where registered against a primary official source. Substantive support is not asserted without a separate proof. Applicability is never inferred from citation presence.**

This separation is mandatory for future Conductellence development.

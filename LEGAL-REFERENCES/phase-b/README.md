# Phase B — Semantic Support Proof

**Programme:** `CDX-PROG-LEGAL-BD-001`  
**Authority:** `CDX-CLR-LEGAL-BD-001`  
**Household state:** DISPATCHED / IN_PROGRESS

Phase B converts the current reference-only legal map into reviewed support relationships without allowing citation relevance to masquerade as legal support.

## Operating rule

Every paragraph × provision edge begins as `CONTEXTUAL`. Each edge must receive one of four dispositions:

1. `KEEP_CONTEXTUAL` — exact legal provision remains relevant, but no stronger support is asserted.
2. `PROMOTE_DERIVED_WITH_PROOF` — a verified proof records the exact external proposition, the Conductellence extension, and the boundary of that extension.
3. `PROMOTE_TEXTUAL_WITH_PROOF` — a verified proof establishes material proposition-level equivalence.
4. `REMOVE_REFERENCE` — the provision does not provide sufficient relevance and is removed from the paragraph.

No automated process may infer dispositions 2 or 3 from keyword similarity.

## Household process

Janitor checks queue completeness, source identity, orphan references, proof syntax and inconsistent states. Handyman may repair only deterministic J1 defects such as mismatched IDs or regenerated indices. Semantic equivalence and disputed legal meaning are J2.

Director may close Phase B only when the queue has no unresolved items and all stronger relationships have verified proofs.

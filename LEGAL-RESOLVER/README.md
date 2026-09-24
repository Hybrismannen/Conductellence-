# Phase C — Legal Applicability Resolver

**Programme:** `CDX-PROG-LEGAL-BD-001`  
**Authority:** `CDX-CLR-LEGAL-BD-001`  
**Household state:** CLEARED_PENDING_B

Phase C separates legal applicability from citation relevance and semantic support.

The resolver is deliberately fail-safe:

- missing facts → `UNKNOWN`;
- no exact reviewed rule → `UNKNOWN`;
- disputed classification/conflict → `LEGAL_REVIEW_REQUIRED`;
- citation presence alone → no applicability result;
- model confidence → no applicability result.

The deterministic rule registry is initially empty. This is intentional. A rule is admitted only after the relevant legal scope conditions have been specifically reviewed and represented.

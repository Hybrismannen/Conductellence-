# Phase D — Regulatory Drift & Temporal Legal State

**Programme:** `CDX-PROG-LEGAL-BD-001`  
**Authority:** `CDX-CLR-LEGAL-BD-001`  
**Household state:** CLEARED_PENDING_C

Phase D preserves the difference between **what law was represented as being at a historic execution time** and **what the current external legal state is understood to be now**.

## Initial implementation

The bootstrap implementation deliberately separates:

1. source identity;
2. source reachability;
3. content/fingerprint drift;
4. confirmed legal change;
5. interpretation of legal effect.

Only 1–2 are initially automated here.

A failed fetch is not repeal. A redirect is not amendment. A changed HTML page is not automatically a legal change. All such events are findings or drift candidates until properly classified.

## Future provider adapters

Provider-specific adapters may later capture official metadata, amendment relations, ELI metadata, national SFS relationships, authoritative corrigenda and implementation acts. Such adapters must preserve the raw observed fact separately from the legal interpretation.

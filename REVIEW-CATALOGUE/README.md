# Conductellence Review Catalogue

The Review Catalogue governs all `CDX-LAW-001` provisions that are not fully machine-decidable.

## Canonical review classes

- `CDX-REV-PARTIAL-001` — deterministic prechecks + authorised human judgment.
- `CDX-REV-HUMAN-001` — human judgment required.
- `CDX-REV-LEGAL-001` — qualified legal review required.
- `CDX-REV-CONSTITUTIONAL-001` — constitutional decision reserved to authorised human constitutional authority.

The review engine validates a decision record. It does not create substantive authority and must never emit autonomous `ALLOW`.

Every accepted review should be persisted using `review-record.schema.json` and, where consequential, referenced by SPETL.

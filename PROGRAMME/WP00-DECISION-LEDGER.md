# CDX-WP00 — Decision Ledger

Status: HISTORICAL DECISIONS CONSOLIDATED FOR WP01  
Date: 2026-10-28

This ledger records decisions that materially shaped Conductellence/CDX. It does not by itself amend constitutional state.

| ID | Decision | First/decisive source | Current standing |
|---|---|---|---|
| D-001 | Conductellence is an independent root governance authority, not an FFOS subsystem. | CHAT-002; reaffirmed CHAT-009 | ACTIVE |
| D-002 | HCC and Ex-Inerta Libertad belong in Conductellence as source appendices/lineage and may be referenced by Pius. | CHAT-002; CHAT-010 | ACTIVE |
| D-003 | CDX is law-first, with the Conductellence Act as constitutional law layer. | CHAT-003 | ACTIVE |
| D-004 | Legal claims require real, granular legal sources; hallucinated provisions are prohibited. | CHAT-003/004 | ACTIVE |
| D-005 | Legal Integrity B–D is governed; no auto-judgment or hard-stop bypass. | CHAT-004 | ACTIVE |
| D-006 | Scientific evidence may support claims but cannot become legal/constitutional authority merely by being evidence. | CHAT-005 | ACTIVE |
| D-007 | Machine-decidable and human-review law must both have operational paths: 69 automatable + 62 review-governed = 131/131. | CHAT-008; PRs #11–#12 | ACTIVE |
| D-008 | Independent SPETL evidence preservation is required before production enforcement claims. | CHAT-006/008; PR #13 | ACTIVE_BLOCKER |
| D-009 | Repository constitutional integrity requires native protection beyond in-repo detection/CI. | CHAT-006; PR #8 | ACTIVE_BLOCKER |
| D-010 | Core remediation does not equal production enforcement; CDX remains PRE_RELEASE / BOOTSTRAP until closure criteria are met. | CHAT-008/009 | ACTIVE |
| D-011 | Canonical name derivation is “Code of Conduct + Excellence.” | CHAT-011 | ACTIVE |
| D-012 | `CDX` is the sole canonical shorthand; `CEX` is superseded. | CHAT-011 | ACTIVE |
| D-013 | Canonical local integration hook is `.cdx/anchor.json`; legacy `.security/conductellence.json` is migration provenance only. | CHAT-011 | ACTIVE |
| D-014 | Governance is asymmetric bidirectional: CDX publishes governance; governed repos retain local anchors and local enforcement. CDX is not a universal super-admin. | CHAT-011/012 | ACTIVE |
| D-015 | FFOS is the first serious canonical anchor/runtime integration target, but anchor verification does not itself prove runtime enforcement. | CHAT-012 | ACTIVE |
| D-016 | CareerHub/Grace/Weronika uses of Conductellence are downstream/manual integration cases, not constitutional sources or automatic certification. | CHAT-013/014 | ACTIVE_BOUNDARY |
| D-017 | Barnombudet is explicitly outside the CDX dependency/control tree. | CHAT-015 | ACTIVE_EXCLUSION |
| D-018 | Pius lineage is preserved without collapsing Pius ontology/governance into CDX runtime architecture. | CHAT-010/016 | ACTIVE |
| D-019 | Pius Universe anchor may be declared while remaining NOT_VERIFIED for runtime purposes. | CHAT-016; PR #16 | ACTIVE |
| D-020 | FFC/Motherpher form-flode remains pending admission until canonical anchor and verification land. | CHAT-017; PR #16 | ACTIVE |
| D-021 | Estate registry inclusion does not imply identical governance or runtime enforcement. | Current master-control chat, 2026-10-28 | ACTIVE |
| D-022 | Target estate topology is 31 known repositories → 31 registry records → applicability classification → canonical anchor where applicable → verification → CDX 1.0 propagation. | Current master-control chat, 2026-10-28 | ACTIVE |

## Decision status vocabulary

- **ACTIVE** — preserved as current architectural or governance intent.
- **ACTIVE_BLOCKER** — current requirement that blocks a stronger release/enforcement claim.
- **ACTIVE_BOUNDARY** — constrains where CDX authority or certification may be claimed.
- **ACTIVE_EXCLUSION** — explicitly outside the CDX governance dependency.
- **SUPERSEDED** — historical state retained for provenance but no longer valid.

## Superseded decision forms

- CEX as a parallel shorthand → **SUPERSEDED by D-012**.
- “Conduct of Excellence” as canonical name derivation → **SUPERSEDED by D-011**.
- CDX embedded inside FFOS → **SUPERSEDED by D-001/D-014**.
- repository anchor = runtime enforcement → **SUPERSEDED by D-010/D-015**.
- local SPETL chain = independent evidence custody → **SUPERSEDED by D-008**.
- legacy security manifest as canonical anchor → **SUPERSEDED by D-013**.

## WP01 use

WP01 must test every ACTIVE decision against current `main`, issues, merged PRs, live anchors and machine-readable state. Where repository state differs, WP01 must classify the difference as:
- repository drift,
- historical wording drift,
- incomplete implementation,
- obsolete decision,
- or genuine constitutional conflict.

No conflict should be silently normalized.

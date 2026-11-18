# Google Drive Security Framework v1.1 — CDX Alignment and Implementation Handoff

**Status:** DESIGN PROPOSAL / NOT ADOPTED / NO PRODUCTION HARD-GATE.
**Owner:** Director · **Underlying Director policy:** OAI-DRIVE-APPEND-ONLY-001 v1.0.
**New policy candidate:** https://docs.google.com/document/d/1jjimsADzcACFioQEbq98eXOsv1_sO5GGNv2_ma-Qdjw/edit (v1.1 DRAFT in My Drive root policy folder).
**Existing v1.0 source:** https://docs.google.com/document/d/18nexuzVfOEWwM7vXcPcB1NkjQHsEGKWxZHSqo-qlBRs/edit — intentionally unchanged.

## Existing CDX source authority

Read actual main sources: `LAW/CONDUCTELLENCE-ACT.md` (Principles I, III, VI; 3 § / 4 §; 4–5 kap; 7–8 kap; 13–17 kap); `RUNTIME-INTEGRATION/CDX-RUNTIME-001.json`; `POLICY/control-registry.json`; `POLICY/engine.py`; `REVIEW-CATALOGUE/README.md`; `SPETL/README.md`; `SECURITY-TWIN/README.md`; `GOVERNANCE/constitutional-change-policy.md`; `GOVERNANCE/system-state.json`; `GOVERNANCE/release-boundary-v1.json` and `GOVERNANCE/CDX-1.0-RESIDUAL-OBLIGATIONS.json`.

**Interpretation:** A Drive consumer must have a local enforcing gateway. CDX remains its policy/authority provenance. A README, GitHub anchor, PR or reference runtime is not equivalent to a production effect guard. CDX 1.0 constitutional topology is frozen; use existing policy/control/review/SPETL/estate surfaces instead of inventing a new constitutional domain.

## Non-negotiable effect requirements

- READ task-authorized content; CREATE_NEW only under exact approved parent IDs; a creation transaction can initialize content, but then the new Drive ID must be SEALED as pre-existing.
- UPDATE_EXISTING, DELETE, TRASH, MOVE/RENAME, PERMISSION, ACL, COMMENT, DOCS/SHEETS/SLIDES BATCH UPDATE, BULK SYNC, ROLLBACK or other mutations: REQUIRE_HUMAN, deny before effect without authenticated exact-target/operation authorization.
- A create method can still be abused. Verify request body, path, target ID, allowed root, OAuth principal, content hash, idempotency nonce and origin/binding of resumable upload session URLs.
- Strictly separate the read principal, narrow create principal and isolated, disabled-by-default mutation executor. An AI workflow cannot be its own approver.
- Every attempt emits pre-effect SPETL. Every successful effect emits post-effect evidence, independently preserved. Record blocked actions too. Missing policy, authority, signed approval or independent evidence = restrictive outcome.
- No client outside the registered gateway may hold a usable privileged writer credential. A ChatGPT setting applies only to that ChatGPT plugin and not unrelated Google OAuth apps.
- Privileged owner identity is fundamentally outside any claim that Google Drive has native create-only enforcement. Provider IAM and human control remain a distinct boundary.

## Proposed deterministic control and review mapping

| Action | Policy decision | Preconditions |
|---|---|---|
| READ | ALLOW_WITH_CONTROLS | Identity, task mandate, authorized source, minimization and private output |
| CREATE_NEW | ALLOW_WITH_CONTROLS | Approved parent ID, new-object intent, no use of update endpoints, verified session and seal |
| EDIT or any existing-object mutation | REQUIRE_HUMAN until authenticated exact-scope approval; DENY if absent | Target ID, version, effect diff, authority, approval one-time nonce, recheck |
| DELETE / TRASH / PURGE | REQUIRE_HUMAN; additional irreversible-effect review | Exact itemized manifest, higher-strength human confirmation and no auto cleanup |
| Permission or ownership change | REQUIRE_HUMAN; treat as high consequence | ACL diff, identity, data-risk review |
| Ambiguous/missing policy, unknown OAuth identity or evidence failure | SECURITY_STOP / DENY | No provider effect |

**Important:** do not directly merge this as a new v1.0 control-registry entry. Before actual CDX policy extension, provide explicit review of compatibility, test vectors, constitutional boundary, sovereign approval and release pinning. Existing `POLICY/proposals/OAI-DRIVE-APPEND-ONLY-001.json` is a proposal, not active law or registry.

## Security framework work packages

**GD-01 Govern:** classify personal My Drive vs Google Workspace and linked organizational access. Register policy source, Director authority, third-party restrictions, exception procedure. CDX constitutional scope decision.

**GD-02 Identify:** enumerate every live consumer, grant, Google OAuth client, account, scope, secrets, root IDs, folders, REST/Docs/Sheets/Slides methods, agents, scripts and sync clients; build Security Twin graph and risk inventory. Unknown consumer = NOT HARDGATED.

**GD-03 Protect:** implement a single trust boundary for machine Drive writes; least-privileged principals and authorized parent registry; a deterministic pre-effect policy decision; replay-resistant session registry for resumable upload; isolated human mutation executor with TTL and one-time approval; no broad credentials in consumer jobs.

**GD-04 Detect:** SPETL pre/post evidence, independent custody, Google Drive changes.list/watch where available, backup/permission drift checks; alert on unapproved edits. Notifications only DETECT, not PREVENT.

**GD-05 Respond:** stop, revoke, preserve evidence, impact report, Director escalation. Never automatically 'fix' by changing existing Drive content.

**GD-06 Recover:** encrypted independent backups under approved retention; simulate restore into NEW harmless test location; require Director approval for any in-place restore.

**GD-07 Verify:** synthetic negative tests across the full mutations matrix; prove no alternate write path. Distinguish tested client vs all-client coverage; exact commit/policy pins and independent security review.

**GD-08 Activate:** CDX protected PR approval and merge, governed downstream rollouts, provider-side token/permission reconciliation and independent Director acceptance before marking `DRIVE_HARDGATE_VERIFIED`.

## Existing implementation gap

The FFOS/FF-Spatial draft upload allowlists and offline tests cover method-level denial but do not yet bind each resumable upload URI to the specific create transaction, verify approved parent against a signed Director allowlist or exhaustively enumerate alternative OAuth clients. Their CI PASS is not production enforcement. The FFOS cloud-drive integration remained live acceptance HOLD in its existing main architecture.

## Acceptance constraints

Do not present 'system-wide hard gate' until (1) every machine writer path is inventoried, blocked or guarded; (2) read/create success and all mutation negative cases are observed before provider effects; (3) human approval cannot be forged or reused; (4) SPETL independent readback verified; (5) restore drill passed; (6) CDX constitutional review completed; and (7) Director signs the exact release/effect boundary.

## External source distinctions

Google's own OAuth documentation states `drive.file` permits creation and modification of certain files; it is **not** a native create-only scope: https://developers.google.com/workspace/drive/api/guides/api-specific-auth

Google documents Drive `changes.list` and `changes.watch` for change observation: https://developers.google.com/workspace/drive/api/guides/manage-changes

NIST CSF 2.0 provides the Govern/Identify/Protect/Detect/Respond/Recover analytical structure, **not** CDX authority: https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final

## Scope rule

This document is a **new additive proposal** within the already open branch `policy/openai-drive-create-only-20261118`. Do not change existing v1.0 records or claim accepted status. CDX approval is reserved to the Director through the protected repository process.

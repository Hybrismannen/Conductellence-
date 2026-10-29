# CDX WP05 — Post-Configuration Evidence Reconciliation (2026-10-29)

**Evidence class:** USER-OBSERVED-GITHUB-UI / UNATTESTED PLATFORM ADMIN READBACK  
**Repository:** `Hybrismannen/Conductellence-` · protected target `main`  
**Disposition:** `RULE_CREATED_AND_UI_READBACK_MATCHES_TARGET / INDEPENDENT_API_VERIFICATION_PENDING`  
**Release authority:** none; `CDX-BLOCK-REPO-PROTECTION-001` remains open in canonical source until audited platform evidence is accepted.

## Newly observed evidence

The repository owner provided screenshots in the governing conversation showing GitHub's success banner **“Branch protection rule created.”**, followed by the reopened saved `main` rule showing **“Applies to 1 branch.”** The saved configuration displays:
- Pull request required before merge;
- ordinary GitHub approving reviews not required; human-sovereign approval is instead a separately required check;
- strict branch up-to-date requirement;
- exact five GitHub Actions checks: `constitutional-audit`, `mutation-guard`, `readiness`, `state-reconciliation`, `human-sovereign-approval`;
- conversation resolution required;
- administrator bypass disabled;
- force pushes and deletions disabled.

These observations are consistent with `GOVERNANCE/repository-protection-target.json`. The repository was independently discovered with `visibility=public` in the connected GitHub repository metadata earlier in this execution sequence. Thus the historic statement asserting the repository **is private** and requires a plan upgrade is stale or factually inapplicable.

## Canonical current GitHub file readback

Direct connected-GitHub readback still finds:
- `GOVERNANCE/repository-protection-state.json`: `branch_protected_flag=false`, `branch_protection_verified=false`, `PLATFORM_PLAN_GATE_BLOCKED`;
- `GOVERNANCE/repository-protection-verification.json`: `PENDING_PLATFORM_CAPABILITY`, seven verification criteria false, rule identifier null;
- `GOVERNANCE/system-state.json`: WP05 blocker open, CDX `PRE_RELEASE`, WP07 `BLOCKED_EXTERNAL_GATES`;
- `GOVERNANCE/release-preflight-state.json`: release not authorized, explicit requirement for independent pre-merge protection platform readback.

These records predate the owner's protection configuration. They are not updated or overridden by this observation-only note.

## Independent verification gap and mandatory actions

The installed GitHub connector exposes neither `GET /repos/{owner}/{repo}/branches/main/protection` nor a ruleset administrative read method. The screenshots prove a saved configuration was visible in the owner's authenticated UI but **do not** independently attest the underlying platform identifier, enforcement against a test PR, or current API state. The immutable GitHub control-plane attestation remains absent.

Authorized repository administrator / independently authorized verifier should:
1. Read `GET /repos/Hybrismannen/Conductellence-/branches/main/protection` using a GitHub credential with repository administration-read permission, and record HTTP status, observation time, relevant settings and the GitHub-generated rule identifier when available.
2. Verify the five required status contexts and their GitHub Actions app source, strict freshness, PR requirement, human status gate, conversation resolution, non-bypass, force-push and deletion restrictions against `GOVERNANCE/repository-protection-target.json`.
3. Perform a non-destructive negative test from a disposable PR or verified platform rules inspector that an unapproved/missing-status change cannot merge. Do not bypass or push directly to main.
4. Record independent signed/attributed evidence in `repository-protection-verification.json`; only if fully supported transition `repository-protection-state.json`, then `system-state.json` and `release-preflight-state.json` through a separately reviewed PR with required statuses and human-sovereign approval.
5. Re-run `AUDITS/audit_repository_protection.py`, the canonical release preflight, and WP07 candidate/CI verification on the exact review head.

## Governance decisions

- **WP05:** `CONFIGURED_UI_OBSERVED / INDEPENDENT_ENFORCEMENT_PENDING`.
- **CDX WP07:** `BLOCKED_EXTERNAL_GATES`; no release tag, no `RELEASED`, and no authorization inferred.
- **FFOS F8.7:** `HOLD_EXTERNAL_GOVERNANCE`; no runtime promotion.
- **CDX frozen topology:** unchanged; no policy, authority class, constitutional section or canonical state redefinition.

This record must not be represented as a closure attestation.

## Required-check workflow repair (same draft PR)

The mandatory `state-reconciliation` check was pending because `.github/workflows/cdx-estate-registry-consistency.yml` previously restricted pull-request triggers to `ESTATE-REGISTRY/**`, `GOVERNANCE/system-state.json` and the workflow itself. An `AUDITS/**`-only PR could never receive that required check. The workflow's `pull_request` trigger now covers every PR against `main`, retaining its `verify-cdx-registry.py` execution and unchanged path-scoped `push` trigger. This is a candidate fix only: exact-head GitHub Actions results have not yet been verified. The approval status must be reissued for the final head by the human owner, and no release/blocker status is promoted.

## Required-check negative-gate observation

A later authenticated owner screenshot of draft PR #40 displays four successful required GitHub Actions checks (`constitutional-audit`, `mutation-guard`, `readiness`, `state-reconciliation`) and `human-sovereign-approval` as **Expected — Waiting for status to be reported**. The merge surface remains unavailable while the PR is Draft. This is operational evidence that the configured required-check contexts are recognized; it is **not yet a non-draft merge-denial test**, nor a platform-admin API readback of all restrictions. Unrelated Vercel is failing because the account is blocked; it is not a CDX release attestation.

The installed connector exposes no branch-protection administrative GET method. The separate public API attempt from this environment could not establish a usable authenticated admin read. Therefore do not mark the canonical `branch_protection_verified` true on this evidence. A reviewer with GitHub administrator-read authority must record the required settings from the actual GitHub API (or obtain a verifiable equivalent), then test enforcement before promoting WP05. WP07 remains `BLOCKED_EXTERNAL_GATES`.

## Authenticated platform API evidence — 2026-10-29

The repository owner executed authenticated `gh api repos/Hybrismannen/Conductellence-/branches/main/protection` and supplied the response. Raw response SHA-256: `7a1cc17239a34dde4a6145f2f98a7b048b2a131999bad005396db2d6e18b799f`; 1602 bytes. This is a user-provided authenticated GitHub REST response, not independently re-fetched by the ChatGPT connector.

Confirmed from response: exact five required status contexts `constitutional-audit`, `human-sovereign-approval`, `mutation-guard`, `state-reconciliation`, `readiness`, each GitHub Actions app ID 15368; strict up-to-date status `true`; administrator enforcement `true`; force pushes `false`; deletions `false`; conversation resolution `true`; PR review protection object present with ordinary approvals count 0. Screenshots confirm rule targets main and applies to one branch. The screenshot PR #40 separately confirms four technical contexts produced success and human-sovereign-approval was pending.

**Material target discrepancy requiring disposition:** `required_pull_request_reviews.dismiss_stale_reviews=false` in the API, while target says `true`. Zero ordinary approval reviews and exact-head human approval context mitigate normal stale-review risk, but do not silently satisfy the literal target. Reconcile as a justified target correction or change setting through authorized human GitHub configuration, then repeat readback. No signed/platform-independent final enforcement negative test is provided, and no platform-assigned rule ID is present in response.

**Disposition:** `AUTHENTICATED_API_SETTINGS_CONFIRMED / TARGET_DIFFERENCE_AND_INDEPENDENT_NEGATIVE_TEST_PENDING`. Do not yet set WP05 `blocker_closed=true` or authorize WP07 on this record.

## Target reconciliation and enforcement verification protocol

The human-directed execution has reconciled `GOVERNANCE/repository-protection-target.json` with the authenticated owner GitHub API snapshot: the canonical zero-review model now explicitly treats ordinary review dismissal as non-applicable, while the `human-sovereign-approval` status remains required on the exact PR head commit. This is **not** a removal of the human approval requirement.

**Still missing:** authenticated independent non-draft merge-denial check for the withheld human status, or verified read-only platform enforcement equivalence; the user-provided admin API readback does not alone prove merge rejection behavior. Safe verifier procedure: create a separate disposable PR containing only a benign audit fixture, leave human status absent, make the PR ready for review, observe the protected merge endpoint refusing merge with the required check pending, record head SHA, time, screenshots/API output and close the fixture PR unmerged. Never attempt a bypass, forced push, release tag, or direct mutation to main. Do not use the WP05 evidence PR itself for the test, because it contains meaningful security workflow changes. If this requires human action or unavailable platform permissions, retain HOLD.

**Current decisions:** `WP05=AUTHENTICATED_SETTINGS_VERIFIED_NEGATIVE_TEST_PENDING`; `WP07=BLOCKED_EXTERNAL_GATES`; `F8.7=HOLD_EXTERNAL_GOVERNANCE`. The previously committed canonical system and preflight blockers must remain in place until new evidence has passed independent review and the actual governing merge controls.

## Non-draft negative-test fixture — PR #41

A separate non-draft disposable PR (#41, https://github.com/Hybrismannen/Conductellence-/pull/41) was created from `main` at head SHA `503796552ce7bc94320c5f4d1c49171c7a77678b`. It adds only `AUDITS/fixtures/wp05-merge-denial-20261029.txt`; no authorization comment was issued and no merge was performed. CI readback shows the Constitutional Mutation Guard, Remediation Readiness and Law Audit workflows completed successfully. The `state-reconciliation` trigger repair is still only on PR #40, so PR #41 does not establish that status reporting until #40 is merged. `human-sovereign-approval` is deliberately withheld. The connected API lacks an authenticated branch merge eligibility/denial read, so definitive non-draft merge-block evidence is pending the owner-side GitHub PR #41 merge box or authenticated rules evaluation. Close PR #41 unmerged after capturing this evidence. **WP05 and WP07 remain on hold until independent evidence acceptance.**

# CDX-WP05 — Native Repository Protection

**Status:** MAXIMUM IN-REPO HARDENING COMPLETE — EXTERNAL PLATFORM GATE REMAINS  
**Blocker:** `CDX-BLOCK-REPO-PROTECTION-001`  
**Date:** 2026-10-28

## 1. Objective

WP05 must establish **pre-merge** protection for the constitutional default branch. The existing in-repository controls are necessary but insufficient because a failing post-push workflow cannot prevent a direct mutation from having already reached `main`.

## 2. Current controls

The repository already uses:

- `.github/CODEOWNERS`;
- Conductellence Law Audit;
- Constitutional Mutation Guard;
- Remediation Readiness;
- constitutional change/mutation policies;
- PR provenance checks for protected-surface commits.

These controls reduce risk and provide evidence, but they do not constitute native branch protection.

## 3. Platform observation

On 2026-10-28:

- the repository is private;
- the rulesets API returned HTTP 403:
  **“Upgrade to GitHub Pro or make this repository public to enable this feature.”**
- branch-protection inspection returned HTTP 403:
  **“Resource not accessible by integration.”**
- the connected GitHub integration exposes no administration capability to enable protection.

This is a real platform/account boundary, not a missing repository file.

## 4. Non-actions

Conductellence will not:

- make the repository public automatically;
- alter GitHub plan/billing automatically;
- treat the post-push mutation guard as equivalent to pre-merge prevention;
- remove blocker #5 because CI is green.

## 5. Closure criteria

Blocker #5 may close only after the repository owner enables native/equivalent protection and CDX can verify all of:

1. pull request required for `main`;
2. Conductellence Law Audit required;
3. Constitutional Mutation Guard required;
4. human approval required;
5. force pushes disabled;
6. branch deletion disabled;
7. protection re-read from the platform and recorded as verified.

## 6. Programme state

WP05 repository-side hardening is complete, but the blocker remains open under:

`PLATFORM_PLAN_GATE_BLOCKED`

No release or enforcement promotion follows.

Required external action: enable private-repository GitHub protection capability (e.g. GitHub Pro or another owner-approved configuration) and then resume WP05 verification.


## 7. WP05 execution — 2026-10-29

A fresh platform re-read confirmed:

- repository visibility: `private`;
- repository owner permission: `admin`;
- `main.protected=false`;
- branch protection API: HTTP 403 `Resource not accessible by integration`;
- rulesets API: HTTP 403 `Upgrade to GitHub Pro or make this repository public to enable this feature`;
- the installed ChatGPT GitHub integration exposes no branch/ruleset administration action;
- plugin discovery found no alternative GitHub administration connector.

No public-visibility or billing/plan mutation was attempted.

### Repository-side hardening completed

WP05 now adds:

- canonical target profile: `GOVERNANCE/repository-protection-target.json`;
- platform verification record: `GOVERNANCE/repository-protection-verification.json`;
- dedicated fail-closed audit: `AUDITS/audit_repository_protection.py`;
- protection audit wired into Law Audit and Remediation Readiness;
- reconciled CODEOWNERS coverage across all protected constitutional surfaces;
- `.github/CODEOWNERS` itself included in the mutation guard;
- owner-bound human approval workflow: `.github/workflows/human-sovereign-approval.yml`;
- approval context: `human-sovereign-approval`.

### Human approval without a second reviewer account

For a protected PR, the repository owner may comment:

`/cdx-approve`

The default-branch approval workflow emits `human-sovereign-approval=success` on the PR's exact head SHA. A later commit changes the SHA and requires a new approval. `/cdx-revoke` marks the same context failed.

This becomes enforceable only when the branch protection/ruleset requires that context before merge.

## 8. Exact platform configuration required

Once private-repository protection is available, configure `main` to require:

1. pull request before merge;
2. required status `constitutional-audit`;
3. required status `mutation-guard`;
4. required status `readiness`;
5. required status `state-reconciliation`;
6. required status `human-sovereign-approval`;
7. current branch before merge / strict status evaluation;
8. no force push;
9. no branch deletion;
10. no uncontrolled administrator/actor bypass.

Then perform an independent platform re-read and populate `GOVERNANCE/repository-protection-verification.json`.

Only after that re-read may:

- `satisfies_enforcing_requirement=true`;
- `CDX-BLOCK-REPO-PROTECTION-001` close;
- WP07 move from `BLOCKED_EXTERNAL_GATES` to `READY_FOR_HUMAN_RELEASE_DECISION`.

## 9. Current determination

WP05 has completed every safe repository-side action available through the connected tooling.

The remaining step is an **owner-controlled GitHub account/platform action**, not missing Conductellence code.

Therefore the correct state remains:

`MAXIMUM_IN_REPO_HARDENING_COMPLETE / PLATFORM_PLAN_GATE_BLOCKED`


## 10. Human approval control observation

A disposable pull request (#38) was created solely to test the owner-bound approval mechanism and was not merged.

Observed evidence:

- PR head: `c9b06c2e3fcff17e4a57d7bc4fddd5a5d616b324`;
- owner command: `/cdx-approve`;
- workflow: `Conductellence Human Sovereign Approval`;
- workflow run: `40788804123` — PASS;
- approver: `Hybrismannen`;
- emitted context: `human-sovereign-approval`;
- emitted state: `success`;
- status bound to the exact PR head SHA;
- test PR closed unmerged.

This proves the human-approval control itself works. It does **not** close #5 because GitHub still does not require that status, the constitutional audits or PR-only mutation before merge.

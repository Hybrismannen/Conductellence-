# CDX-WP05 — Native Repository Protection

**Status:** COMPLETE — VERIFIED NATIVE PROTECTION  
**Former blocker:** `CDX-BLOCK-REPO-PROTECTION-001` — CLOSED  
**Closure date:** 2026-10-29  
**Canonical verification:** `GOVERNANCE/repository-protection-verification.json`

## 1. Objective

WP05 establishes **pre-merge protection** for the constitutional default branch so protected Conductellence surfaces cannot reach `main` without the required CDX controls.

The required path is:

```text
working branch
→ pull request
→ required CDX status checks
→ human sovereign approval
→ protected merge to main
```

## 2. Closure result

WP05 is complete.

Native classic branch protection for `main` was verified through owner-authenticated GitHub platform evidence and independently promoted through PR #42.

The verified protection requires:

1. pull request before merge;
2. strict/current-branch status evaluation;
3. `constitutional-audit`;
4. `mutation-guard`;
5. `readiness`;
6. `state-reconciliation`;
7. `human-sovereign-approval`;
8. administrator enforcement;
9. force pushes disabled;
10. branch deletion disabled;
11. conversation resolution before merge;
12. no uncontrolled bypass path.

The canonical verification record reports:

- `state=VERIFIED`;
- `all_criteria_verified=true`;
- `satisfies_enforcing_requirement=true`;
- `protection_rule_id=CLASSIC_BRANCH_RULE_MAIN`;
- authenticated platform response SHA-256:
  `7a1cc17239a34dde4a6145f2f98a7b048b2a131999bad005396db2d6e18b799f`.

## 3. Human sovereign approval control

The approval workflow is:

`.github/workflows/human-sovereign-approval.yml`

For a protected PR, the repository owner comments:

`/cdx-approve`

The workflow emits:

`human-sovereign-approval=success`

on the pull request's exact head SHA.

A later commit changes the SHA and therefore requires a new approval. `/cdx-revoke` revokes the status.

Control evidence:

- PR #38 — approval mechanism test;
- head `c9b06c2e3fcff17e4a57d7bc4fddd5a5d616b324`;
- workflow run `40788804123` — PASS;
- test PR closed unmerged.

## 4. Negative-gate evidence

PR #41 was used as a non-draft negative-gate test.

Observed result:

`MERGE_BUTTON_DISABLED_WHILE_TWO_REQUIRED_STATUSES_MISSING`

The PR was closed unmerged.

The test did not isolate the human-approval status because `state-reconciliation` was also absent. It nevertheless demonstrated that the native branch gate prevented merge while required statuses were unsatisfied.

## 5. Evidence promotion

PR #40 reconciled saved branch-protection UI/platform evidence.

PR #42 then promoted the canonical WP05 state after:

- owner-authenticated GitHub branch-protection readback;
- independent evidence review;
- required CDX CI;
- explicit `/cdx-approve` on the exact PR head;
- protected merge to `main`.

PR #42 merged as:

`a6b916e7c3fa33a7c5638b9f119be1dfce17c130`

and removed `CDX-BLOCK-REPO-PROTECTION-001` from the core release blocker set.

## 6. Current live readback

On 2026-10-29, the public repository branch endpoint reports:

- `main.protected=true`;
- protection enabled;
- required status checks enforced for `everyone`;
- required contexts:
  - `constitutional-audit`;
  - `human-sovereign-approval`;
  - `mutation-guard`;
  - `state-reconciliation`;
  - `readiness`.

The connected GitHub App still cannot read the administration-only branch-protection subresources. That connector limitation does not negate the separately preserved owner-authenticated verification evidence used for WP05 closure.

## 7. Resulting programme state

The core release blocker set is now empty.

WP05 completion therefore permits WP07 to operate from:

`READY_FOR_HUMAN_RELEASE_DECISION`

subject to the separate release-decision and publication gates.

WP05 completion does **not** by itself imply:

- `release_state=RELEASED`;
- `enforcement_state=ENFORCEMENT_READY` or `ENFORCING`;
- estate-wide runtime binding;
- WP08–WP14 completion.

## 8. Reopening condition

`CDX-BLOCK-REPO-PROTECTION-001` must be reopened if the verified protection ceases to hold, including if:

- `main` becomes unprotected;
- any required CDX status is removed;
- PR-only protection is removed;
- human sovereign approval ceases to be required;
- force push or branch deletion becomes permitted;
- an uncontrolled bypass path is introduced.

Repository visibility alone is not the control. The governing condition is continued verified pre-merge protection.

# CDX-WP05 — Native Repository Protection

**Status:** EXTERNAL PLATFORM GATE — BLOCKER REMAINS OPEN  
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

WP05 implementation analysis is complete, but the blocker remains open under:

`PLATFORM_PLAN_GATE_BLOCKED`

No release or enforcement promotion follows.

Required external action: enable private-repository GitHub protection capability (e.g. GitHub Pro or another owner-approved configuration) and then resume WP05 verification.

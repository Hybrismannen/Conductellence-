# Constitutional Mutation Policy

**Policy ID:** `CDX-GOV-CONST-MUT-001`

Protected constitutional surfaces:

- `LAW/**`
- `INTERPRETATION/**`
- `appendices/**`
- `POLICY/**`
- `CONTROL-CATALOGUE/**`
- `GOVERNANCE/**`
- `SPETL/**`
- `SECURITY-TWIN/**`
- `GLOBAL-AUTHORITY-CORPUS/**`
- `LEGAL-REFERENCES/**`
- `LEGAL-RESOLVER/**`
- `REGULATORY-DRIFT/**`
- `EVIDENCE-AUTHORITY/**`
- `REVIEW-CATALOGUE/**`
- `RED-TEAM/**`
- `DISTRIBUTION/**`
- `RUNTIME-INTEGRATION/**`
- `ESTATE-REGISTRY/**`
- `AUDITS/**`
- `.github/CODEOWNERS`
- `.github/workflows/**`

Required process:

```text
working branch
→ pull request
→ Conductellence audits
→ human review/merge
→ main
```

Direct mutation of protected surfaces on `main` is a constitutional process violation.

GitHub branch/ruleset enforcement is currently an external platform capability. Until branch protection is available and enabled, Conductellence uses CODEOWNERS plus a direct-push tripwire, but this is a degraded control because a failing post-push workflow cannot prevent the commit from having landed.

Therefore `constitutional amendment path protected` remains **NOT SATISFIED FOR ENFORCING MODE** until native pre-merge repository protection is enabled.

## CDX 1.0 release-boundary freeze

During `CDX-RC01-BOUNDARY-001`, the protected surface also carries a scope constraint: closure work may repair and harden existing domains, but a new first-class CDX domain or a change to the frozen constitutional topology requires an explicit human-approved boundary exception under `GOVERNANCE/release-boundary-v1.json`.


## Human sovereign approval gate

For protected-surface pull requests, the canonical human approval signal is the commit status context `human-sovereign-approval`.

The status is emitted only by the default-branch workflow `.github/workflows/human-sovereign-approval.yml` after the repository owner comments exactly:

`/cdx-approve`

on an open pull request targeting `main`.

The approval is bound to the pull request's exact head SHA. Any later commit creates a new SHA and therefore requires a new approval. The owner may revoke the status with `/cdx-revoke`.

This approval mechanism becomes a **pre-merge control only when GitHub branch protection/rulesets require the `human-sovereign-approval` status on `main`**. Until that platform rule is active and independently verified, the repository-protection blocker remains open.

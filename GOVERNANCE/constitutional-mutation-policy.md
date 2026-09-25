# Constitutional Mutation Policy

**Policy ID:** `CDX-GOV-CONST-MUT-001`

Protected constitutional surfaces:

- `LAW/**`
- `appendices/**`
- `POLICY/**`
- `CONTROL-CATALOGUE/**`
- `GOVERNANCE/enforcement-state.json`
- `LEGAL-REFERENCES/**`
- `LEGAL-RESOLVER/**`

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

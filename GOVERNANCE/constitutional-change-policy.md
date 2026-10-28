# Constitutional Change Policy

**Policy ID:** CDX-CONST-CHANGE-001  
**Authority:** HUMAN_SOVEREIGN_AUTHORITY  
**Applies to:** Conductellence constitutional and enforcement surfaces.

## Protected surfaces

Changes to the following are constitutionally material:

- `LAW/**`
- `INTERPRETATION/**`
- `appendices/**`
- `GOVERNANCE/**`
- `CONTROL-CATALOGUE/**`
- `POLICY/**`
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

## Required path

Constitutionally material change shall use:

```text
human-authorised proposal
→ non-authoritative branch
→ pull request
→ constitutional/technical CI
→ human review
→ merge
```

Direct mutation of `main` is non-conforming even where GitHub account capabilities do not technically prevent it.

## Platform limitation

Repository-side policy cannot substitute for GitHub branch protection. Until branch protection/rulesets are externally enabled and verified, Conductellence shall remain unable to satisfy the production-enforcement criterion `constitutional amendment path protected`.

CI therefore treats the lack of verified platform protection as an **ENFORCING blocker**, not as permission to weaken the rule.

## Constitutional adoption process

Constitutional maturity transitions use the canonical state sequence:

```text
FOUNDATIONAL_DRAFT
→ CONSTITUTIONAL_CANDIDATE
→ STABLE_CANDIDATE
→ ADOPTED
→ AMENDED
```

Adoption requires explicit `HUMAN_SOVEREIGN_AUTHORITY`, a frozen release boundary, passing constitutional/technical CI and a preserved adoption record. Candidate and adopted constitutional states do not imply system release or production enforcement. Final adoption shall be recorded by a machine-readable order in `GOVERNANCE/orders/` and shall not waive independent release/enforcement blockers.

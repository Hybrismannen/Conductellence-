# Runtime Integration Contract

**Contract ID:** `CDX-RUNTIME-001`

A repository backlink and CI audit establish governance binding. They do **not** establish runtime enforcement.

A governed runtime reaches `VERIFIED_RUNTIME_BOUND` only when consequential execution follows:

```text
intent
→ identity / authority / mandate context
→ applicable Conductellence enforcement surface
→ policy evaluation
→ ALLOW / restrictive decision
→ SPETL evidence
→ effect only when permitted
→ reconciliation
```

## Required adapter properties

1. **Fail closed.** Policy service/runtime error may not become ALLOW.
2. **No implicit authority.** Context carries explicit `authority_ref` and `mandate_ref`.
3. **Policy pinning.** Decision records policy version and control results.
4. **Evidence before completion.** Consequential action produces SPETL decision evidence.
5. **External effect mediation.** SEND/PUBLISH/DEPLOY and equivalent effects require the applicable release gate.
6. **Revocation.** Current revocation/suspension state is checked before consequential effect.
7. **Content-authority separation.** Tool, model, prompt, file or external content cannot grant authority.
8. **Local enforcement.** Conductellence is not a universal super-admin; the governed system owns its enforcement point.
9. **Testability.** Each adapter provides allow, deny and policy-unavailable regression cases.

## Integration states

- `BOUND_PENDING_RUNTIME_INTEGRATION`
- `BOUND_CI_MONITORED`
- `RUNTIME_GUARDED_UNVERIFIED`
- `VERIFIED_RUNTIME_BOUND`

Only the final state satisfies estate runtime enforcement readiness.

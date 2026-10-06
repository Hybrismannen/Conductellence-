# Runtime Integration Contract

**Contract ID:** `CDX-RUNTIME-001`  
**Canonical system short name:** `CDX`

A repository backlink and CI audit establish governance binding. They do **not** establish runtime enforcement.

Before any governed system can claim Conductellence runtime integration, it must satisfy the CDX Estate Anchor Standard (`CDX-GOV-ANCHOR-001`) and maintain a canonical local anchor at:

```text
.cdx/anchor.json
```

The governing relationship is:

```text
CDX  ──publishes governance──>  governed system
CDX  <──local anchor / hook───  governed system
```

The anchor establishes the technical governance relationship. Runtime integration then proves that consequential execution actually follows that relationship.

A governed runtime reaches `VERIFIED_RUNTIME_BOUND` only when consequential execution follows:

```text
intent
→ identity / authority / mandate context
→ pinned CDX governance context
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
10. **CDX anchor continuity.** Runtime policy context must reconcile with the repository/system's declared `.cdx/anchor.json`; divergence degrades or invalidates the claimed binding.

## Integration states

- `BOUND_PENDING_RUNTIME_INTEGRATION`
- `BOUND_CI_MONITORED`
- `RUNTIME_GUARDED_UNVERIFIED`
- `VERIFIED_REFERENCE_RUNTIME` — local pinned policy bundle + tested repository guard; does not prove application runtime mediation.
- `VERIFIED_RUNTIME_BOUND` — consequential application/runtime enforcement point verified with SPETL evidence

`VERIFIED_REFERENCE_RUNTIME` satisfies reference-runtime distribution readiness. Only `VERIFIED_RUNTIME_BOUND` satisfies production estate runtime enforcement readiness.

## Anchor versus runtime state

CDX anchor state and runtime integration state are separate axes.

A repository can be `CDX_BOUND` without having a consequential runtime. A system that does have consequential execution cannot be `VERIFIED_RUNTIME_BOUND` unless its CDX anchor is valid and its local enforcement point is verified.

See [`../GOVERNANCE/CDX-ESTATE-ANCHOR-STANDARD.md`](../GOVERNANCE/CDX-ESTATE-ANCHOR-STANDARD.md).

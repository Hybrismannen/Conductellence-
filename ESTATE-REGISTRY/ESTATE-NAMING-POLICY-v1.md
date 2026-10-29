# CDX Estate — Terminology, Scope and Binding Policy v1.0

**Policy ID:** CDX-ESTATE-TERMS-001  
**Status:** OWNER-ACCEPTED TERMINOLOGY / IMPLEMENTATION CANDIDATE  
**Authority source:** Conductellence (CDX-SYS-001)  
**Membership source:** `ESTATE-REGISTRY/registry-v2.json` (or its formally adopted successor)  
**Date:** 2026-10-29

## Governing rule

**Estate** is the canonical term for the set of digital repositories, systems, agents and other registered work surfaces **subject to Conductellence applicability**. An Estate is a **governance and applicability boundary**, not a legal company, a corporate group, a claim of intellectual-property ownership, a deployed runtime, or a grant of permission.

The CDX Estate is defined by the canonical CDX Estate Registry's applicability decisions, **not** by GitHub owner, organization name, repository proximity, a product name, a declaration from an agent, an inferred subsidiary relationship or a downstream manifest alone. The Estate can include separately owned, independently authoritative, domain-specific systems and development projects. CDX publishes governing requirements; each applicable consumer owns its local enforcement point.

## Terminology and hierarchy

1. **CDX Estate:** The current set of work surfaces classified `GOVERNED_APPLICABLE` in the authoritative registry. `AUTHORITY_SOURCE` identifies CDX itself; it is not another ordinary consumer. `EXCLUDED_BY_DECISION` is outside CDX applicability, and `HISTORICAL_ALIAS` is provenance, not a separate currently governed object.
2. **Estate member / consumer:** A canonical, current registered repository/system with an applicable classification. Its own domain repository retains authority over its content and products, subject to its CDX obligations.
3. **Estate segment:** A human-readable grouping (for example Form & Flöde-related activity, Pius, or another business/project grouping). It is not a new legal entity, independent constitutional authority or source of membership decisions. Such segments must resolve back to registry identities.
4. **Agent operating context:** The agent's owning/consuming system, governing principal, applicable registered Estate member, policy/security binding and host/runtime. An agent's self-declared context is a proposal until the host independently resolves and verifies it.
5. **CDX anchor:** The local `.cdx/anchor.json` binding governed by CDX-GOV-ANCHOR-001, where the canonical registry requires it. An Estate terminology reference document is **not** an anchor.

## Applicability and exceptions

- `GOVERNED_APPLICABLE` members MUST preserve the prescribed CDX repository anchor obligation, subject to the registry's specific anchor and runtime classifications.
- Agents operating as instances of applicable Estate consumers MUST be bound to the requisite CDX governance interface before admission to that consumer's runtime. Read-only/data-sensitive behavior remains subject to the applicable policy; an E0 label does not waive governance.
- `EXCLUDED_BY_DECISION` members MUST NOT be enrolled, synchronized or controlled by CDX merely because they are discoverable, public, owned by an adjacent account, or associated with a user. The explicit exclusion of `Hybrismannen/Barnombudet` is preserved.
- `HISTORICAL_ALIAS` records MUST NOT be counted or anchored as independent live repositories. Preserve identity lineage.
- External distribution of reusable architectures or agent templates (including AMA) MAY omit the *source Estate's* CDX binding only when the recipient is demonstrably outside the source Estate and explicitly defines its own governance authority, mandates and policy/security boundary. Such distribution does not modify the source Estate Registry, remove an existing applicable consumer's CDX obligation, or waive core authorization/evidence requirements.
- An agent MUST NOT establish its own Estate membership, external status or exception by choosing an identifier such as `FF_ESTATE` or `EXTERNAL`. Host-verified registration and authority determine applicability. Unresolved membership/authority MUST fail closed for consequential operations.

## Architectural boundaries and source precedence

1. CDX canonical law/policy and adopted decisions govern applicability. `ESTATE-REGISTRY/registry-v2.json` (or successor) supplies the current member classification.
2. Domain repositories (FFC, FFOS, Pius and others) remain canonical for their respective domain content, operations and versions. CDX is not an unrestricted superadministrator.
3. Repository-local references may mirror this policy ID and the exact registry classification but MUST NOT maintain a competing membership list, redefine exclusions, create fictitious operating authorities or claim verified runtime enforcement.
4. The Estate Registry distinguishes **applicability**, **anchor requirement**, **anchor state**, **runtime screening** and **runtime verification**. None implies the next. In particular: declaration is not installation; installation is not verification; CI monitoring is not effect mediation; release is not estate-wide enforcement.
5. Changing the Estate's applicability or exclusions requires a separately governed CDX registry decision, not a terminology patch or a downstream agent's configuration.

## Distribution and acceptance

This rule is accepted as terminology policy by the owner. Its rollout is tracked through repository change requests and source validation. Repository-local files record **policy awareness only**; they do not install anchors, change rights, bind host runtime, prove compliance or merge themselves. Formal production admission remains subject to the established CDX gates.

**Registry reference at drafting:** WP08 Registry v2, observed 2026-10-29: 31 identifiers / 30 current objects, 28 applicable consumers, one excluded current repository and one authority source. Treat these figures as a dated snapshot, never a permanently encoded cardinality.

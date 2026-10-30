# Conductellence — CDX 1.0

> **A constitutional governance and runtime-control system for non-human digital execution.**  
> CDX turns human authority into explicit, bounded, auditable machine execution — without allowing models, agents, tools or repositories to invent their own mandate.

**Canonical system:** CDX-SYS-001 · **Law:** CDX-LAW-001 · **Release:** 1.0.0 · **Programme:** final-accepted

---

## What CDX is

Conductellence (**CDX = Code of Conduct + Excellence**) is the governance layer for the digital estate.

It answers five questions before a non-human system is allowed to create a consequential effect:

1. **Who is acting?**
2. **Under whose authority?**
3. **What mandate and capability permit the action?**
4. **What policy applies at this boundary?**
5. **What evidence proves what was decided and what actually happened?**

CDX is therefore not only a policy document. It is a connected system of law, controls, runtime decisions, evidence, estate registration, security state and audit.

~~~mermaid
flowchart LR
    H[Human mandate] --> A[Authority]
    A --> P[Principal]
    P --> C[Capability]
    C --> R[CDX runtime decision]
    R -->|ALLOW / ALLOW_WITH_CONTROLS| E[Local effect]
    R -->|Restrictive decision| B[Block / hold / quarantine]
    R --> S[SPETL evidence]
    E --> S
    S --> T[Security Twin / audit]
~~~

**Human sovereign authority remains superior.** CDX governs delegated execution; it does not replace the human authority that grants the mandate.

---

## The core idea

CDX separates things that are often incorrectly collapsed into one another:

~~~text
identity ≠ authority
capability ≠ mandate
repository membership ≠ runtime enforcement
policy decision ≠ effect
effect ≠ acceptance
reference runtime ≠ production consumer runtime
release ≠ estate-wide enforcement
~~~

The governing chain is:

~~~text
human mandate
→ authority
→ principal
→ capability
→ information / model / tool
→ attempted execution
→ boundary decision
→ local effect
→ evidence
→ responsibility
~~~

---

## How CDX works

CDX uses an **asymmetrical bidirectional governance model**.

~~~mermaid
flowchart TB
    CDX[CDX canonical authority]
    LAW[Law + interpretation]
    POL[Controls + policy]
    EST[Estate registry]
    CON[Governed consumer]
    ANC[Local .cdx/anchor.json]
    RUN[Local enforcement point]
    EVD[SPETL evidence]

    CDX --> LAW
    LAW --> POL
    CDX --> EST
    POL --> CON
    EST --> CON
    CON --> ANC
    ANC --> CDX
    CON --> RUN
    RUN --> EVD
    EVD --> CDX
~~~

CDX publishes the constitutional source, policy contracts and runtime requirements. Each governed repository keeps its own local anchor and owns its own enforcement points.

CDX is **not** a universal super-admin with unrestricted write access across every repository.

---

## Runtime decision loop

The production contract is [CDX-RUNTIME-001@1.0.0](RUNTIME-INTEGRATION/CDX-RUNTIME-001.json).

~~~mermaid
sequenceDiagram
    participant H as Human / Director
    participant F as Governed runtime
    participant C as CDX policy
    participant S as SPETL evidence
    participant X as External/local effect

    H->>F: Mandated intent
    F->>F: Resolve identity, authority, mandate, scope
    F->>C: Evaluate pinned CDX policy
    C-->>F: Seven-way decision
    alt ALLOW / ALLOW_WITH_CONTROLS
        F->>S: PRE_EFFECT evidence
        F->>F: Re-check current authority / policy / revocation
        F->>X: Perform bounded effect
        F->>S: POST_EFFECT evidence
    else restrictive decision
        F->>S: BLOCKED evidence
        F-->>H: Deny / hold / quarantine / stop
    end
~~~

CDX has seven canonical runtime outcomes:

| Decision | Meaning |
|---|---|
| ALLOW | Effect may proceed. |
| ALLOW_WITH_CONTROLS | Effect may proceed only after required obligations are verified. |
| REQUIRE_HUMAN | Human decision or approval is required. |
| QUARANTINE | Isolate the action or object pending review. |
| DENY | Action is not permitted. |
| SECURITY_STOP | Security/trust prerequisites are unavailable or invalid. |
| CONSTITUTIONAL_STOP | Action conflicts with constitutional authority or governing law. |

Policy failure is fail-closed. Missing authority, invalid anchors, unavailable policy, unknown operators or unavailable required evidence cannot silently become permission.

---

## What CDX contains

| Layer | Function | Canonical area |
|---|---|---|
| **Law** | Normative internal constitutional rules | [LAW/](LAW/) |
| **Interpretation** | Meaning, edge cases and precedent | [INTERPRETATION/](INTERPRETATION/) |
| **Controls** | Machine-addressable law → control mappings | [CONTROL-CATALOGUE/](CONTROL-CATALOGUE/) |
| **Policy** | Executable control registry / policy-as-code | [POLICY/](POLICY/) |
| **Review governance** | Human-review obligations for non-automatable rules | [REVIEW-CATALOGUE/](REVIEW-CATALOGUE/) |
| **Runtime integration** | Versioned consumer execution contract | [RUNTIME-INTEGRATION/](RUNTIME-INTEGRATION/) |
| **SPETL** | Decision, effect, incident and assurance evidence | [SPETL/](SPETL/) |
| **Security Twin** | Authority, reachability, dependency and blast-radius state | [SECURITY-TWIN/](SECURITY-TWIN/) |
| **Estate Registry** | Which repositories are governed, excluded or historical | [ESTATE-REGISTRY/](ESTATE-REGISTRY/) |
| **Evidence authority** | Who may produce, preserve and verify evidence | [EVIDENCE-AUTHORITY/](EVIDENCE-AUTHORITY/) |
| **Legal Resolver** | Fail-safe legal reference resolution | [LEGAL-RESOLVER/](LEGAL-RESOLVER/) |
| **Regulatory Drift** | Tracks changes in authoritative external sources | [REGULATORY-DRIFT/](REGULATORY-DRIFT/) |
| **Red Team** | Adversarial acceptance and abuse cases | [RED-TEAM/](RED-TEAM/) |
| **Distribution** | Portable CDX 1.0 runtime/policy artifacts | [DISTRIBUTION/](DISTRIBUTION/) |
| **Governance** | State, adoption, protection, orders and system rules | [GOVERNANCE/](GOVERNANCE/) |
| **Programme** | Historical construction record and final reports | [PROGRAMME/](PROGRAMME/) |

For the full system walk-through, read the **[CDX 1.0 System Guide](GOVERNANCE/CDX-1.0-SYSTEM-GUIDE.md)**.

---

## Estate model

The current CDX estate is registry-driven — not inferred from GitHub organization, repository names or agent claims.

At CDX 1.0 programme closure:

| Estate measure | State |
|---|---:|
| Known repository identifiers | **31** |
| Unique current repository objects | **30** |
| CDX authority source | **1** |
| Governed current repositories | **28** |
| Governed anchors CDX_BOUND / PASS | **28 / 28** |
| Pending admissions | **0** |
| Explicit exclusions | **1** |
| Historical aliases | **1** |

Every governed current repository carries a canonical .cdx/anchor.json pinned to CDX 1.0.

The anchor proves governance binding. It **does not by itself prove runtime enforcement**.

---

## Current system state

CDX state is deliberately represented on independent axes.

| Axis | State | What it means |
|---|---|---|
| Constitutional | **ADOPTED** | CDX-LAW-001 v1.0.0 is formally adopted. |
| Core runtime | **VERIFIED_REFERENCE_RUNTIME** | The canonical reference runtime is implemented and verified. |
| Release | **RELEASED** | CDX 1.0.0 is a published stable release. |
| Estate governance | **COMPLETE** | Registry, anchors, verification and admissions are complete. |
| Programme | **FINAL_ACCEPTED_WITH_RESIDUAL_DOWNSTREAM_OBLIGATIONS** | CDX 1.0 construction is finished. |
| Estate integration | **BINDINGS_IN_PROGRESS** | Production consumer runtime rollout is still being completed. |
| Enforcement | **BOOTSTRAP** | Estate-wide consequential enforcement is not yet claimed. |

Machine-readable truth is [GOVERNANCE/system-state.json](GOVERNANCE/system-state.json).

**Maturity is not enforcement. Release is not integration. Integration is not estate-wide enforcement.**

---

## How a governed system uses CDX

A repository does not copy CDX law and become a new authority. It binds to a released CDX version.

~~~text
1. Registry classifies repository as governed
2. Repository installs .cdx/anchor.json
3. Anchor pins CDX release + policy digest
4. CI verifies repository/anchor continuity
5. Consequential runtime identifies local effect points
6. Runtime provides explicit authority_ref + mandate_ref
7. Pinned CDX policy evaluates the attempted action
8. Restrictive outcomes fail closed
9. PRE_EFFECT evidence is preserved
10. Local effect executes only after permission
11. POST_EFFECT evidence is preserved
12. Independent verification may promote runtime standing
~~~

A repository can therefore be **CDX_BOUND** without being **VERIFIED_RUNTIME_BOUND**.

---

## What CDX protects against

The architecture is designed to prevent or expose:

- implicit authority;
- identity being treated as permission;
- agents granting themselves broader mandates;
- capability escalation;
- hidden or unregistered execution paths;
- model identity substituting for accountable principal identity;
- policy bypass when a service is unavailable;
- boundary crossings without evidence;
- unverified external effects;
- silent replay after uncertain effects;
- evidence generated solely by the actor being audited;
- repository drift away from the released governance source;
- estate-wide enforcement claims based only on CI or documentation.

---

## Assurance model

CDX does not accept “the code exists” as sufficient evidence.

~~~text
constitutional integrity
+ control coverage
+ policy tests
+ adversarial tests
+ repository protection
+ evidence custody
+ runtime-effect tests
+ estate reconciliation
+ human sovereign approval
~~~

The terminal programme audit is [AUDITS/CDX-1.0-TERMINAL-AUDIT-2026-10-30.md](AUDITS/CDX-1.0-TERMINAL-AUDIT-2026-10-30.md).

The full end report is [PROGRAMME/CDX-1.0-END-REPORT-2026-10-30.md](PROGRAMME/CDX-1.0-END-REPORT-2026-10-30.md).

---

## What CDX is not

CDX is **not**:

- state legislation;
- a substitute for qualified legal advice;
- an autonomous authority above the human principal;
- an agent;
- a universal repository administrator;
- a reason to centralize every application runtime;
- proof of production enforcement merely because a repository has an anchor;
- permission for a system to accept or certify its own consequential work.

Applicable external law and fundamental rights remain superior wherever they apply.

---

## Start here

### Understand the system

1. [CDX 1.0 System Guide](GOVERNANCE/CDX-1.0-SYSTEM-GUIDE.md)
2. [Conductellence Act](LAW/CONDUCTELLENCE-ACT.md)
3. [State Model](GOVERNANCE/state-model.md)
4. [Runtime Contract](RUNTIME-INTEGRATION/CDX-RUNTIME-001.json)

### Integrate a repository

1. [Estate Anchor Standard](GOVERNANCE/CDX-ESTATE-ANCHOR-STANDARD.md)
2. [Anchor Template](DISTRIBUTION/cdx-anchor.template.json)
3. [Estate Registry v2](ESTATE-REGISTRY/registry-v2.json)

### Inspect assurance

1. [AUDITS/](AUDITS/)
2. [SPETL/](SPETL/)
3. [SECURITY-TWIN/](SECURITY-TWIN/)
4. [RED-TEAM/](RED-TEAM/)

---

## CDX 1.0 programme boundary

The numbered CDX 1.0 construction programme ended at **WP15**.

Further work belongs to one of four paths:

- consumer runtime rollout under CDX-RUNTIME-001;
- maintenance of the released system;
- a governed constitutional/policy amendment;
- a separately initiated future CDX release programme.

The historical work-package record remains in [PROGRAMME/](PROGRAMME/), but the repository front page now describes **the system that exists**, not the sequence used to build it.

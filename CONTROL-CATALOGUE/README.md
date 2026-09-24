# Conductellence Control Catalogue

The Control Catalogue is the machine-addressable bridge between `CDX-LAW-001` and implementation.

The binding chain is:

```text
Chapter + §
    ↓
Control ID
    ↓
Policy / Protocol / Schema
    ↓
Enforcement Point
    ↓
Audit ID
    ↓
Evidence
```

## Binding states

- **BOOTSTRAP_BOUND** — the § has named control/audit objects, but runtime effectiveness is not implied.
- **UNBOUND_BOOTSTRAP** — the § exists and has an auditability class, but operational binding has not yet been built.
- **IMPLEMENTED** — implementation exists and passes structural acceptance.
- **VERIFIED** — implementation has passed defined assurance tests.
- **DEGRADED** — previously verified control is no longer fully trusted.
- **REVOKED** — control is no longer authorized for current use.

The current registry is [law-bindings.json](law-bindings.json).

No dashboard may represent `BOOTSTRAP_BOUND` as equivalent to `VERIFIED`.

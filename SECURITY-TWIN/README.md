# Security Twin

**System ID:** `CDX-SYS-003`

The Security Twin is a derived graph, not a second source of truth.

Canonical inputs:
- `ESTATE-REGISTRY/systems.json`
- `POLICY/control-registry.json`
- later: SPETL runtime observations and active identity/capability/tool/data edges.

Generate it with:

`python3 SECURITY-TWIN/build_twin.py`

The generated `SECURITY-TWIN/twin.json` may be treated as disposable projection state. Runtime production deployments should build a current graph from canonical registries plus SPETL observations.

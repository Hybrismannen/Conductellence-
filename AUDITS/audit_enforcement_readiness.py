#!/usr/bin/env python3
from pathlib import Path
import json

state=json.loads(Path("GOVERNANCE/enforcement-state.json").read_text())
bindings=json.loads(Path("CONTROL-CATALOGUE/law-bindings.json").read_text())
protection=json.loads(Path("GOVERNANCE/repository-protection-state.json").read_text())
estate=json.loads(Path("ESTATE-REGISTRY/systems.json").read_text())
adversarial=json.loads(Path("RED-TEAM/scenarios.json").read_text())

full=[s for s in bindings["sections"] if s["auditability"]=="FULLY_AUTOMATABLE"]
implemented=[s for s in full if s.get("binding_state") in {"IMPLEMENTED","VERIFIED"} and s.get("controls") and s.get("audits")]

checks={
 "fully_automatable_control_binding":len(implemented)==len(full)==69,
 "policy_decision_layer":Path("POLICY/engine.py").exists() and Path("POLICY/control-registry.json").exists(),
 "evidence_plane":Path("SPETL/spetl.py").exists(),
 "security_twin":Path("SECURITY-TWIN/build_twin.py").exists(),
 "constitutional_appendices":Path("appendices/APP-A-HCC/README.md").exists() and Path("appendices/APP-B-EX-INERTA-LIBERTAD/README.md").exists(),
 "global_authority_corpus":Path("GLOBAL-AUTHORITY-CORPUS/authority-registry.json").exists(),
 "critical_adversarial_acceptance":adversarial.get("state")=="ACTIVE" and len(adversarial.get("scenarios",[]))>=15 and Path("AUDITS/audit_adversarial_acceptance.py").exists(),
 "constitutional_amendment_path_protected":protection.get("satisfies_enforcing_requirement") is True,
 "estate_runtime_integration":all(s.get("security_state") in {"CONTROLLED","VERIFIED_RUNTIME_BOUND"} for s in estate.get("systems",[]))
}

internal_keys=[
 "fully_automatable_control_binding","policy_decision_layer","evidence_plane",
 "security_twin","constitutional_appendices","global_authority_corpus",
 "critical_adversarial_acceptance"
]
core_reference_runtime_ready=all(checks[k] for k in internal_keys)
full_enforcing_ready=all(checks.values())
blockers=[k for k,v in checks.items() if not v]

if state.get("mode")=="ENFORCING" and not full_enforcing_ready:
    raise SystemExit("FAIL ENFORCING claimed with blockers: "+", ".join(blockers))
if state.get("core_reference_runtime_state")=="REMEDIATED" and not core_reference_runtime_ready:
    raise SystemExit("FAIL REMEDIATED core state claimed without all internal criteria")

print(json.dumps({
 "mode":state.get("mode"),
 "core_reference_runtime_state":state.get("core_reference_runtime_state"),
 "fully_automatable":len(full),
 "implemented":len(implemented),
 "core_reference_runtime_ready":core_reference_runtime_ready,
 "full_enforcing_ready":full_enforcing_ready,
 "checks":checks,
 "blockers":blockers
},indent=2))
print("PASS: enforcement state accurately separates core remediation from full estate enforcement")

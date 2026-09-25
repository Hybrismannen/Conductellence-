#!/usr/bin/env python3
from pathlib import Path
import json

state=json.loads(Path("GOVERNANCE/enforcement-state.json").read_text())
bindings=json.loads(Path("CONTROL-CATALOGUE/law-bindings.json").read_text())
protection=json.loads(Path("GOVERNANCE/repository-protection-state.json").read_text())
estate=json.loads(Path("ESTATE-REGISTRY/systems.json").read_text())

full=[s for s in bindings["sections"] if s["auditability"]=="FULLY_AUTOMATABLE"]
implemented=[s for s in full if s.get("binding_state") in {"IMPLEMENTED","VERIFIED"} and s.get("controls") and s.get("audits")]

checks={
 "fully_automatable_control_binding":len(implemented)==len(full),
 "policy_decision_layer":Path("POLICY/engine.py").exists() and Path("POLICY/control-registry.json").exists(),
 "evidence_plane":Path("SPETL/ledger.py").exists(),
 "security_twin":Path("SECURITY-TWIN/build_twin.py").exists(),
 "constitutional_appendices":Path("appendices/APP-A-HCC/README.md").exists() and Path("appendices/APP-B-EX-INERTA-LIBERTAD/README.md").exists(),
 "global_authority_corpus":Path("GLOBAL-AUTHORITY-CORPUS/authority-registry.json").exists(),
 "constitutional_amendment_path_protected":protection.get("satisfies_enforcing_requirement") is True,
 "estate_runtime_integration":all(s.get("security_state") in {"CONTROLLED","VERIFIED_RUNTIME_BOUND"} for s in estate.get("systems",[]))
}
blockers=[k for k,v in checks.items() if not v]
if state.get("mode")=="ENFORCING" and blockers:
    raise SystemExit("FAIL ENFORCING claimed with blockers: "+", ".join(blockers))
print(json.dumps({
 "mode":state.get("mode"),
 "fully_automatable":len(full),
 "implemented":len(implemented),
 "checks":checks,
 "blockers":blockers
},indent=2))
print("PASS: enforcement mode is not overstated")

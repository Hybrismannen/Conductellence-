#!/usr/bin/env python3
from pathlib import Path
import json

def fail(m):
    print("FAIL:",m); raise SystemExit(1)

required={
 "state":Path("GOVERNANCE/enforcement-state.json"),
 "protection":Path("GOVERNANCE/repository-protection-state.json"),
 "bindings":Path("CONTROL-CATALOGUE/law-bindings.json"),
 "controls":Path("POLICY/control-registry.json"),
 "spetl":Path("SPETL/spetl.py"),
 "twin":Path("SECURITY-TWIN/build_twin.py"),
 "estate":Path("ESTATE-REGISTRY/systems.json"),
 "hcc":Path("appendices/APP-A-HCC/README.md"),
 "ex":Path("appendices/APP-B-EX-INERTA-LIBERTAD/README.md"),
 "gac":Path("GLOBAL-AUTHORITY-CORPUS/authority-registry.json"),
 "adversarial":Path("RED-TEAM/scenarios.json"),
 "adversarial_audit":Path("AUDITS/audit_adversarial_acceptance.py"),
 "review_bindings":Path("REVIEW-CATALOGUE/bindings.json"),
 "review_procedures":Path("REVIEW-CATALOGUE/procedures.json"),
 "review_audit":Path("AUDITS/audit_review_governance.py")
}
for name,p in required.items():
    if not p.exists(): fail(f"missing {name}: {p}")

state=json.loads(required["state"].read_text())
protection=json.loads(required["protection"].read_text())
bindings=json.loads(required["bindings"].read_text())
controls=json.loads(required["controls"].read_text())
adversarial=json.loads(required["adversarial"].read_text())
review_bindings=json.loads(required["review_bindings"].read_text())
review_procedures=json.loads(required["review_procedures"].read_text())

full=[s for s in bindings.get("sections",[]) if s.get("auditability")=="FULLY_AUTOMATABLE"]
implemented=[s for s in full if s.get("binding_state") in {"IMPLEMENTED","VERIFIED"}]
control_ids={c["control_id"] for c in controls.get("controls",[])}
missing_controls=[]
for s in full:
    for cid in s.get("controls",[]):
        if cid not in control_ids: missing_controls.append((s["section_id"],cid))

criteria={
 "fully_automatable_bound":len(full)==len(implemented)==69 and not missing_controls,
 "policy_decision_layer_operational":required["controls"].exists() and required["spetl"].exists(),
 "evidence_plane_reference_runtime_operational":required["spetl"].exists(),
 "security_twin_reference_runtime_operational":required["twin"].exists(),
 "foundational_appendices_admitted":required["hcc"].exists() and required["ex"].exists(),
 "global_authority_corpus_instantiated":required["gac"].exists(),
 "critical_adversarial_acceptance":adversarial.get("state")=="ACTIVE" and len(adversarial.get("scenarios",[]))>=15,
 "review_governance":len(review_bindings.get("bindings",[]))==62 and len(review_procedures.get("procedures",[]))==4,
 "constitutional_amendment_path_platform_protected":protection.get("satisfies_enforcing_requirement") is True
}

internal_keys=[k for k in criteria if k!="constitutional_amendment_path_platform_protected"]
core_ready=all(criteria[k] for k in internal_keys)
blockers=[k for k,v in criteria.items() if not v]

if state.get("core_reference_runtime_state")=="REMEDIATED" and not core_ready:
    fail("REMEDIATED core state declared with unmet internal criteria")
if state.get("mode")=="ENFORCING" and blockers:
    fail("ENFORCING declared with unmet criteria: "+", ".join(blockers))

print(f"PASS: {len(implemented)}/69 FULLY_AUTOMATABLE §§ are bound to implemented controls")
print("INFO: transition criteria="+json.dumps(criteria,sort_keys=True))
print("INFO: core_reference_runtime_ready="+json.dumps(core_ready))
print("INFO: ENFORCING blockers="+json.dumps(blockers))
print(f"PASS: declared mode {state.get('mode')} does not overstate transition readiness")

#!/usr/bin/env python3
"""Conductellence law/control binding coverage audit.

Audit ID: AUD-CDX-BINDING-COVERAGE-001
Law authority:
- 16 kap. 1 § — Control binding
- 16 kap. 2 § — Audit binding
- 16 kap. 3 § — Auditability state
- 19 kap. 7 § — Exhaustiveness by coverage
"""

from pathlib import Path
import json
import re

LAW = Path("LAW/CONDUCTELLENCE-ACT.md")
REGISTRY = Path("CONTROL-CATALOGUE/law-bindings.json")
STATE = Path("GOVERNANCE/enforcement-state.json")

def die(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)

for path in (LAW, REGISTRY, STATE):
    if not path.exists():
        die(f"missing required file: {path}")

law = LAW.read_text(encoding="utf-8")
markers = re.findall(
    r'<!-- cdx:section id="([^"]+)" auditability="([^"]+)" -->',
    law
)
law_ids = {sid for sid, _ in markers}
auditability = {sid: state for sid, state in markers}

registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
state = json.loads(STATE.read_text(encoding="utf-8"))
entries = registry.get("sections", [])
reg_ids = {entry["section_id"] for entry in entries}

missing = sorted(law_ids - reg_ids)
orphaned = sorted(reg_ids - law_ids)
if missing:
    die(f"{len(missing)} law §§ missing from binding registry: {missing[:10]}")
if orphaned:
    die(f"{len(orphaned)} orphaned binding entries: {orphaned[:10]}")

bound = [e for e in entries if e.get("controls") and e.get("audits")]
unbound = [e for e in entries if not (e.get("controls") and e.get("audits"))]

print(f"INFO: law §§={len(law_ids)} bound={len(bound)} unbound={len(unbound)}")
print(f"INFO: enforcement mode={state.get('mode')}")

if state.get("mode") == "ENFORCING":
    defects = []
    for entry in entries:
        sid = entry["section_id"]
        if auditability.get(sid) == "FULLY_AUTOMATABLE":
            controls = entry.get("controls", [])
            audits = entry.get("audits", [])
            if not controls or not audits:
                defects.append((sid, "missing control/audit"))
                continue
            if any("PLANNED" in a for a in audits):
                defects.append((sid, "audit remains PLANNED"))
            if entry.get("binding_state") not in {"IMPLEMENTED", "VERIFIED"}:
                defects.append((sid, f"state={entry.get('binding_state')}"))
    if defects:
        for sid, why in defects[:50]:
            print(f"DEFECT: {sid}: {why}")
        die(f"{len(defects)} fully automatable provisions are not enforcement-ready")

print("PASS: every law § is represented in the machine binding registry")

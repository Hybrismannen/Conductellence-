#!/usr/bin/env python3
"""Conductellence root-structure audit.

Audit ID: AUD-CDX-ROOT-STRUCTURE-001
Law authority:
- 3 kap. 2 § — Repository backlink / canonical authority
- 16 kap. 1-3 §§ — control and audit binding
- 19 kap. 2-3 §§ — versioning and Interpretation Guide
"""

from pathlib import Path
import json

REQUIRED = [
    Path("README.md"),
    Path("LAW/CONDUCTELLENCE-ACT.md"),
    Path("INTERPRETATION/INTERPRETATION-GUIDE.md"),
    Path("CONTROL-CATALOGUE/law-bindings.json"),
    Path("GOVERNANCE/enforcement-state.json"),
]

missing = [str(p) for p in REQUIRED if not p.exists()]
if missing:
    print("FAIL: missing canonical root objects:")
    for item in missing:
        print(f"  - {item}")
    raise SystemExit(1)

state = json.loads(Path("GOVERNANCE/enforcement-state.json").read_text())
if state.get("mode") not in {"BOOTSTRAP", "ENFORCING"}:
    print(f"FAIL: unknown enforcement mode {state.get('mode')}")
    raise SystemExit(1)

readme = Path("README.md").read_text(encoding="utf-8")
if "CDX-SYS-001" not in readme or "CDX-LAW-001" not in readme:
    print("FAIL: README does not identify canonical system and law")
    raise SystemExit(1)

print("PASS: Conductellence canonical root structure present")
print(f"PASS: enforcement mode={state['mode']}")

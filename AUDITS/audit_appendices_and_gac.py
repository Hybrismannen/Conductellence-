#!/usr/bin/env python3
from pathlib import Path
import json

required=[
 "appendices/APP-A-HCC/README.md",
 "appendices/APP-B-EX-INERTA-LIBERTAD/README.md",
 "appendices/APP-C-GLOBAL-AUTHORITY-CORPUS/README.md",
 "GLOBAL-AUTHORITY-CORPUS/authority-registry.json",
]
for x in required:
    if not Path(x).exists():
        raise SystemExit("FAIL missing "+x)

a=Path(required[0]).read_text(encoding="utf-8")
b=Path(required[1]).read_text(encoding="utf-8")
if "HCC-S1-V1.0" not in a or "6721ded6009bd771a22d0ed87444386b3a11d69c740d69828e357f1120abce20" not in a:
    raise SystemExit("FAIL HCC provenance")
if "Ex-Inerta" not in b or "6721ded6009bd771a22d0ed87444386b3a11d69c740d69828e357f1120abce20" not in b:
    raise SystemExit("FAIL Ex-Inerta provenance")
g=json.loads(Path("GLOBAL-AUTHORITY-CORPUS/authority-registry.json").read_text())
if g.get("corpus_id")!="CDX-GAC-001":
    raise SystemExit("FAIL GAC identity")
print("PASS: HCC, Ex-Inerta and Global Authority Corpus appendices are admitted")

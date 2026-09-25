#!/usr/bin/env python3
from pathlib import Path
import json
p=Path("INTERPRETATION/section-records.json")
if not p.exists(): raise SystemExit("FAIL missing interpretation records")
d=json.loads(p.read_text())
if d.get("record_count")!=131 or len(d.get("records",[]))!=131:
    raise SystemExit("FAIL interpretation record count")
ids=[x["section_id"] for x in d["records"]]
if len(ids)!=len(set(ids)): raise SystemExit("FAIL duplicate interpretation section")
if any(not x.get("canonical_text") for x in d["records"]): raise SystemExit("FAIL empty canonical interpretation text")
print("PASS: 131 source-bound interpretation records")

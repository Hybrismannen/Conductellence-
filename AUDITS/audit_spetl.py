#!/usr/bin/env python3
from pathlib import Path
import importlib.util,tempfile

spec=importlib.util.spec_from_file_location("ledger",Path("SPETL/ledger.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

with tempfile.TemporaryDirectory() as td:
    p=Path(td)/"events.jsonl"
    event={"event_type":"POLICY_DECISION","actor_id":"A","action":"READ","decision":"ALLOW","authority_ref":"AUTH","policy_version":"1.0.0","correlation_id":"C","causation_id":"ROOT"}
    m.append_event(p,event)
    ok,count,error=m.verify(p)
    if not ok or count!=1:
        raise SystemExit("FAIL: "+str(error))
print("PASS: SPETL ledger append and verify")

#!/usr/bin/env python3
"""Phase D temporal legal-state/drift integrity audit.

Authority: CDX-CLR-LEGAL-BD-001
"""

from pathlib import Path
import json

STATE=Path("REGULATORY-DRIFT/source-state.json")
PROVISIONS=Path("LEGAL-REFERENCES/legal-provision-registry.json")

def fail(msg):
    print("FAIL:",msg); raise SystemExit(1)

for p in (STATE,PROVISIONS):
    if not p.exists(): fail(f"missing {p}")

state=json.loads(STATE.read_text())
preg=json.loads(PROVISIONS.read_text())
if state.get("authority_ref")!="CDX-CLR-LEGAL-BD-001":
    fail("source-state registry has wrong authority_ref")

sources=state.get("sources",[])
by_url={s["official_url"]:s for s in sources}
if len(by_url)!=len(sources):
    fail("duplicate official_url in source-state registry")

provisions=preg.get("provisions",[])
missing=[p["id"] for p in provisions if p["official_url"] not in by_url]
if missing:
    fail(f"{len(missing)} verified provisions have no Phase D source-state object")

for s in sources:
    if s.get("interpretation_state")!="NO_AUTOMATIC_LEGAL_INTERPRETATION":
        fail(f"{s['source_id']}: automatic legal interpretation unexpectedly enabled")
    if s.get("content_fingerprint") is not None and s.get("content_fingerprint_semantics")=="UNSET":
        fail(f"{s['source_id']}: fingerprint present without declared semantics")

policy=state.get("policy",{})
if "never infer repeal/amendment/inapplicability" not in policy.get("source_failure",""):
    fail("source-failure policy does not explicitly prohibit legal inference")
if "never infer substantive legal change" not in policy.get("fingerprint_change",""):
    fail("fingerprint-change policy does not explicitly prohibit substantive inference")

print(f"PASS: Phase D source-state covers {len(provisions)} provisions across {len(sources)} official source URLs")
print("PASS: source failure/fingerprint drift cannot automatically become legal interpretation")

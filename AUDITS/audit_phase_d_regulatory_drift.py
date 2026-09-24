#!/usr/bin/env python3
"""Phase D regulatory-drift and temporal-state acceptance audit.

Authority: CDX-CLR-LEGAL-BD-001
"""

from pathlib import Path
import json

STATE=Path("REGULATORY-DRIFT/source-state.json")
TEMPORAL=Path("REGULATORY-DRIFT/provision-temporal-state.json")
CHANGES=Path("REGULATORY-DRIFT/confirmed-change-events.json")
PROVISIONS=Path("LEGAL-REFERENCES/legal-provision-registry.json")
CHECKER=Path("REGULATORY-DRIFT/check_source_reachability.py")

def fail(msg):
    print("FAIL:",msg); raise SystemExit(1)

for p in (STATE,TEMPORAL,CHANGES,PROVISIONS,CHECKER):
    if not p.exists(): fail(f"missing {p}")

state=json.loads(STATE.read_text())
temporal=json.loads(TEMPORAL.read_text())
changes=json.loads(CHANGES.read_text())
preg=json.loads(PROVISIONS.read_text())

pids={p["id"] for p in preg["provisions"]}
tmap={x["provision_id"]:x for x in temporal["provisions"]}
if pids!=set(tmap):
    fail(f"temporal registry mismatch missing={len(pids-set(tmap))} orphan={len(set(tmap)-pids)}")

sources=state.get("sources",[])
by_url={s["official_url"]:s for s in sources}
if len(by_url)!=len(sources): fail("duplicate official source URL")
missing=[p["id"] for p in preg["provisions"] if p["official_url"] not in by_url]
if missing: fail(f"{len(missing)} provisions lack source-state coverage")

for s in sources:
    if s.get("interpretation_state")!="NO_AUTOMATIC_LEGAL_INTERPRETATION":
        fail(f"{s['source_id']}: automatic legal interpretation enabled")

for pid,rec in tmap.items():
    for ref in rec.get("source_refs",[]):
        if ref not in pids: fail(f"{pid}: unknown temporal source ref {ref}")
    if rec.get("mode")=="AI_HIGH_RISK_SPLIT":
        branches={b["high_risk_basis"]:b["effective_from"] for b in rec.get("branches",[])}
        if branches.get("ARTICLE_6_2_ANNEX_III")!="2027-12-02":
            fail(f"{pid}: wrong Annex III application date")
        if branches.get("ARTICLE_6_1_ANNEX_I")!="2028-08-02":
            fail(f"{pid}: wrong Annex I application date")

events={e["event_id"]:e for e in changes.get("events",[])}
if "CDX-RDE-2026-AIA-1744" not in events: fail("AI Act 2026 amendment event missing")
if events["CDX-RDE-2026-AIA-1744"].get("effective_from")!="2026-07-27":
    fail("AI Act amendment effective date mismatch")
if "CDX-RDE-2026-SE-CYBER-EFFECT" not in events: fail("Swedish Cybersecurity Act entry-into-force event missing")
if events["CDX-RDE-2026-SE-CYBER-EFFECT"].get("effective_from")!="2026-01-15":
    fail("Swedish Cybersecurity Act entry-into-force date mismatch")

policy=state.get("policy",{})
if "never infer repeal/amendment/inapplicability" not in policy.get("source_failure",""):
    fail("source failure policy permits legal inference")
if "never infer substantive legal change" not in policy.get("fingerprint_change",""):
    fail("fingerprint policy permits substantive inference")

print(f"PASS: temporal state covers all {len(pids)} exact legal provisions")
print(f"PASS: drift source state covers {len(sources)} official primary source URLs")
print("PASS: amended AI Act high-risk application dates are locked to verified current law")
print("PASS: source failure/fingerprint drift cannot become legal interpretation")

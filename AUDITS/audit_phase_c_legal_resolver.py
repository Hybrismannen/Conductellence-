#!/usr/bin/env python3
"""Phase C fail-safe applicability resolver audit.

Authority: CDX-CLR-LEGAL-BD-001
"""

from pathlib import Path
import json
import importlib.util
import tempfile

RULES=Path("LEGAL-RESOLVER/applicability-rules.json")
ENGINE=Path("LEGAL-RESOLVER/resolve_applicability.py")
PROVISIONS=Path("LEGAL-REFERENCES/legal-provision-registry.json")

def fail(msg):
    print("FAIL:",msg); raise SystemExit(1)

for p in (RULES,ENGINE,PROVISIONS):
    if not p.exists(): fail(f"missing {p}")

rules=json.loads(RULES.read_text())
if rules.get("authority_ref")!="CDX-CLR-LEGAL-BD-001":
    fail("applicability rules registry missing clearance authority")

for r in rules.get("rules",[]):
    if not r.get("rule_id") or not r.get("provision_id"):
        fail("registered applicability rule missing identity")
    if r.get("review_state")!="VERIFIED":
        fail(f"{r.get('rule_id')}: non-VERIFIED applicability rule present")
    if r.get("result") not in {"APPLIES","DOES_NOT_APPLY","PARTIALLY_APPLIES","CONDITIONAL"}:
        fail(f"{r.get('rule_id')}: invalid deterministic result")

spec=importlib.util.spec_from_file_location("resolver",ENGINE)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
provision=json.loads(PROVISIONS.read_text())["provisions"][0]["id"]

missing_case={"provision_id":provision,"facts":{"jurisdiction":None,"actor_role":None,"sector":None,"system_class":None,"purpose":None,"unresolved_facts":[]}}
res=mod.resolve(missing_case)
if res["result"]!="UNKNOWN" or res["reasoning_state"]!="MISSING_FACTS":
    fail("resolver does not fail safe on missing facts")

complete_case={"provision_id":provision,"facts":{"jurisdiction":"TEST","actor_role":"TEST","sector":"TEST","system_class":"TEST","purpose":"TEST","unresolved_facts":[]}}
res=mod.resolve(complete_case)
if not rules.get("rules") and (res["result"]!="UNKNOWN" or res["reasoning_state"]!="NO_REGISTERED_RULE"):
    fail("empty rule registry must yield UNKNOWN/NO_REGISTERED_RULE")

conflict_case={"provision_id":provision,"facts":{"jurisdiction":"TEST","actor_role":"TEST","sector":"TEST","system_class":"TEST","purpose":"TEST","unresolved_facts":[],"disputed_classification":True}}
res=mod.resolve(conflict_case)
if res["result"]!="LEGAL_REVIEW_REQUIRED":
    fail("disputed classification must yield LEGAL_REVIEW_REQUIRED")

print("PASS: Phase C resolver fails safe on missing facts, absent rules and disputed classification")
print(f"PASS: {len(rules.get('rules',[]))} deterministic applicability rules are registered")

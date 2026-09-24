#!/usr/bin/env python3
"""Phase C exact-provision Legal Resolver acceptance audit.

Authority: CDX-CLR-LEGAL-BD-001
"""

from pathlib import Path
import importlib.util, json

ENGINE=Path("LEGAL-RESOLVER/resolve_applicability.py")
PROFILES=Path("LEGAL-RESOLVER/scope-profiles.json")
PROVISIONS=Path("LEGAL-REFERENCES/legal-provision-registry.json")
TEMPORAL=Path("REGULATORY-DRIFT/provision-temporal-state.json")

def fail(msg):
    print("FAIL:",msg); raise SystemExit(1)

for p in (ENGINE,PROFILES,PROVISIONS,TEMPORAL):
    if not p.exists(): fail(f"missing {p}")

preg=json.loads(PROVISIONS.read_text())
pids={p["id"] for p in preg["provisions"]}
profiles=json.loads(PROFILES.read_text())["profiles"]
temporal=json.loads(TEMPORAL.read_text())["provisions"]
tids={x["provision_id"] for x in temporal}

if pids != tids:
    fail(f"temporal coverage mismatch missing={len(pids-tids)} orphan={len(tids-pids)}")

prefixes=[p["provision_prefix"] for p in profiles]
if len(prefixes)!=len(set(prefixes)):
    fail("duplicate scope profile prefix")
if {p["profile_id"] for p in profiles}!={"CFR","GDPR","EU-AIA","NIS2","SE-CYBER"}:
    fail("scope profile set must be exactly CFR/GDPR/EU-AIA/NIS2/SE-CYBER")

for prof in profiles:
    for src in prof.get("scope_sources",[]):
        if src not in pids: fail(f"{prof['profile_id']}: unknown scope source {src}")
    for rule in prof.get("outcomes",[]):
        for src in rule.get("source_refs",[]):
            if src not in pids: fail(f"{rule['rule_id']}: unknown source {src}")

spec=importlib.util.spec_from_file_location("resolver",ENGINE)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def check(name,case,expected):
    got=mod.resolve(case)
    if got["result"]!=expected:
        fail(f"{name}: expected {expected}, got {got}")
    if got.get("applicability_inferred_from_citation") is not False:
        fail(f"{name}: citation inference flag not false")
    print(f"PASS CASE: {name} -> {expected}")

check("GDPR no personal data",{
    "provision_id":"GDPR-32-1","legal_snapshot_date":"2026-09-25",
    "facts":{"processes_personal_data":False}
},"DOES_NOT_APPLY")

check("GDPR EU controller current obligation",{
    "provision_id":"GDPR-32-1","legal_snapshot_date":"2026-09-25",
    "facts":{
      "processes_personal_data":True,"material_scope_automated_or_filing":True,
      "legal_actor_role":"CONTROLLER","gdpr_exclusion_outside_union_law":False,
      "gdpr_exclusion_household":False,"gdpr_exclusion_law_enforcement":False,
      "controller_or_processor_established_in_union":True,
      "provision_condition_met":True
    }
},"APPLIES")

check("AI high-risk Annex III before amended application date",{
    "provision_id":"EU-AIA-14-1","legal_snapshot_date":"2026-09-25",
    "facts":{
      "is_ai_system_or_model":True,"ai_actor_role":"PROVIDER",
      "ai_scientific_r_and_d_only":False,"ai_pre_market_research_testing_development":False,
      "ai_personal_nonprofessional_deployer":False,"ai_free_open_source":False,
      "ai_high_risk":True,"ai_article5_or_50":False,
      "provider_union_market_or_service_nexus":True,
      "high_risk_basis":"ARTICLE_6_2_ANNEX_III","provision_condition_met":True
    }
},"DOES_NOT_APPLY")

check("AI Article 50 provider after general application date",{
    "provision_id":"EU-AIA-50-2","legal_snapshot_date":"2026-09-25",
    "facts":{
      "is_ai_system_or_model":True,"ai_actor_role":"PROVIDER",
      "ai_scientific_r_and_d_only":False,"ai_pre_market_research_testing_development":False,
      "ai_personal_nonprofessional_deployer":False,"ai_free_open_source":False,
      "ai_high_risk":False,"ai_article5_or_50":True,
      "provider_union_market_or_service_nexus":True,
      "provision_condition_met":True
    }
},"APPLIES")

check("NIS2 in-scope entity remains national-implementation conditional",{
    "provision_id":"NIS2-21-1","legal_snapshot_date":"2026-09-25",
    "facts":{
      "nis2_annex_entity_type":True,"activities_or_services_in_union":True,
      "medium_or_larger":True,"provision_condition_met":True
    }
},"CONDITIONAL")

check("Swedish municipality cybersecurity duty",{
    "provision_id":"SE-CYBER-2-3-P1","legal_snapshot_date":"2026-09-25",
    "facts":{
      "se_entity_excluded_1_14":False,"se_scope_excluded_under_1_12":False,
      "se_public_operator_type":"MUNICIPALITY","provision_condition_met":True
    }
},"APPLIES")

check("Charter private entity not auto-resolved",{
    "provision_id":"CFR-8-1","legal_snapshot_date":"2026-09-25",
    "facts":{"subject_type":"PRIVATE_ENTITY","provision_condition_met":True}
},"LEGAL_REVIEW_REQUIRED")

check("Missing snapshot date",{
    "provision_id":"GDPR-32-1","facts":{"processes_personal_data":True}
},"UNKNOWN")

print(f"PASS: {len(profiles)} instrument scope profiles validated")
print(f"PASS: exact temporal coverage exists for all {len(pids)} registered provisions")
print("PASS: resolver does not infer applicability from citation presence")

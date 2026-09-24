#!/usr/bin/env python3
"""Fail-safe Conductellence legal applicability resolver.

Authority: CDX-CLR-LEGAL-BD-001
Phase: C

This engine intentionally cannot infer legal applicability from a citation,
keyword similarity, model output or missing facts. It emits UNKNOWN unless an
explicit deterministic applicability rule has been registered. Conflicts and
disputed classifications emit LEGAL_REVIEW_REQUIRED.
"""

from pathlib import Path
import argparse
import json

RULES = Path("LEGAL-RESOLVER/applicability-rules.json")
PROVISIONS = Path("LEGAL-REFERENCES/legal-provision-registry.json")

REQUIRED_FACTS = ("jurisdiction", "actor_role", "sector", "system_class", "purpose")
FINAL_RESULTS = {
    "APPLIES", "DOES_NOT_APPLY", "PARTIALLY_APPLIES", "CONDITIONAL",
    "UNKNOWN", "LEGAL_REVIEW_REQUIRED"
}

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def resolve(case):
    provisions = {p["id"] for p in load(PROVISIONS)["provisions"]}
    rules = load(RULES).get("rules", [])

    provision_id = case.get("provision_id")
    facts = case.get("facts") or {}

    if provision_id not in provisions:
        return {
            "result": "LEGAL_REVIEW_REQUIRED",
            "reasoning_state": "CONFLICT",
            "reasoning_summary": "Provision ID is not present in the verified exact-provision registry.",
            "rule_id": None,
        }

    unresolved = list(facts.get("unresolved_facts") or [])
    missing = [k for k in REQUIRED_FACTS if facts.get(k) in (None, "", [])]
    if unresolved or missing:
        return {
            "result": "UNKNOWN",
            "reasoning_state": "MISSING_FACTS",
            "reasoning_summary": f"Missing/unresolved facts: {sorted(set(missing + unresolved))}",
            "rule_id": None,
        }

    if facts.get("legal_conflict") is True or facts.get("disputed_classification") is True:
        return {
            "result": "LEGAL_REVIEW_REQUIRED",
            "reasoning_state": "CONFLICT",
            "reasoning_summary": "Case contains a disputed legal classification or conflict.",
            "rule_id": None,
        }

    candidates = [r for r in rules if r.get("provision_id") == provision_id]
    if not candidates:
        return {
            "result": "UNKNOWN",
            "reasoning_state": "NO_REGISTERED_RULE",
            "reasoning_summary": "No reviewed deterministic applicability rule is registered for this provision.",
            "rule_id": None,
        }

    matches = []
    for rule in candidates:
        conditions = rule.get("conditions", {})
        if all(facts.get(k) == v for k, v in conditions.items()):
            matches.append(rule)

    if len(matches) == 0:
        return {
            "result": "UNKNOWN",
            "reasoning_state": "NO_REGISTERED_RULE",
            "reasoning_summary": "No registered rule exactly matches the supplied facts.",
            "rule_id": None,
        }

    if len(matches) > 1:
        return {
            "result": "LEGAL_REVIEW_REQUIRED",
            "reasoning_state": "CONFLICT",
            "reasoning_summary": "Multiple deterministic applicability rules match the same case.",
            "rule_id": None,
        }

    rule = matches[0]
    result = rule.get("result")
    if result not in FINAL_RESULTS - {"UNKNOWN", "LEGAL_REVIEW_REQUIRED"}:
        return {
            "result": "LEGAL_REVIEW_REQUIRED",
            "reasoning_state": "CONFLICT",
            "reasoning_summary": "Registered rule contains an invalid deterministic result.",
            "rule_id": rule.get("rule_id"),
        }

    return {
        "result": result,
        "reasoning_state": "DETERMINISTIC_RULE",
        "reasoning_summary": rule.get("reasoning_summary", ""),
        "rule_id": rule.get("rule_id"),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case_json")
    args = ap.parse_args()
    case = load(args.case_json)
    print(json.dumps(resolve(case), indent=2))

if __name__ == "__main__":
    main()

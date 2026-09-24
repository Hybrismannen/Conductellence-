#!/usr/bin/env python3
"""Conductellence paragraph-level legal reference audit.

Audit ID: AUD-CDX-LEGAL-ANCHORS-001
Law authority:
- 2 kap. 5 § — Source authority
- 16 kap. 1-3 §§ — Control/audit binding
- 19 kap. 2 § — Versioning
Policy:
- LEGAL-REFERENCES/LEGAL-REFERENCE-POLICY.md
"""

from pathlib import Path
import json
import re

LAW = Path("LAW/CONDUCTELLENCE-ACT.md")
REGISTRY = Path("LEGAL-REFERENCES/legal-source-registry.json")

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)

if not LAW.exists():
    fail("law file missing")
if not REGISTRY.exists():
    fail("legal source registry missing")

law = LAW.read_text(encoding="utf-8")
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
approved = {s["url"] for s in registry.get("sources", [])}

blocks = re.split(r"\n\s*\n", law)
started = False
issues = []
anchored = 0

def is_prose(block: str) -> bool:
    t = block.strip()
    if not t:
        return False
    if t.startswith("#"):
        return False
    if t.startswith("<!--"):
        return False
    if t.startswith("```"):
        return False
    if t.startswith("> **Legal anchors:**"):
        return False
    if t.startswith("**Canonical law:**") or t.startswith("**Canonical system:**"):
        return False
    if t.startswith("**Version:**") or t.startswith("**Status:**"):
        return False
    if t.startswith("**Adopted into repository:**") or t.startswith("**Language:**"):
        return False
    if re.match(r"^\d+\.\s", t) or t.startswith("- "):
        return False
    if t.startswith(chr(96)) and t.endswith(chr(96)):
        return False
    return True

for i, block in enumerate(blocks):
    if block.strip() == "# Preamble":
        started = True
        continue
    if not started or not is_prose(block):
        continue

    if i + 1 >= len(blocks):
        issues.append(("EOF", block[:100]))
        continue

    anchor = blocks[i + 1].strip()
    if not anchor.startswith("> **Legal anchors:**"):
        issues.append(("MISSING", block[:120].replace("\n", " ")))
        continue

    urls = re.findall(r"\((https://[^)]+)\)", anchor)
    if not urls:
        issues.append(("NO_URL", block[:120].replace("\n", " ")))
        continue

    unknown = [u for u in urls if u not in approved]
    if unknown:
        issues.append(("UNREGISTERED_URL", f"{block[:80]} :: {unknown}"))
        continue

    anchored += 1

if issues:
    for kind, detail in issues[:80]:
        print(f"{kind}: {detail}")
    fail(f"{len(issues)} prose paragraphs violate legal-reference policy")

print(f"PASS: {anchored} prose paragraphs carry registered official legal anchors")
print(f"PASS: {len(approved)} official legal sources registered")

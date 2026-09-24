#!/usr/bin/env python3
"""Conductellence exact legal-reference integrity audit.

Audit ID: AUD-CDX-LEGAL-INTEGRITY-002

This audit is intentionally syntactic and conservative. It does not decide
whether an external law applies to a given system. It verifies that the Act's
legal references are exact, registered, primary-source backed, and consistently
bound to paragraph IDs without generic or ranged citation claims.
"""

from pathlib import Path
import json
import re
import sys

ACT = Path("LAW/CONDUCTELLENCE-ACT.md")
PROVISIONS = Path("LEGAL-REFERENCES/legal-provision-registry.json")
PARA_MAP = Path("LEGAL-REFERENCES/paragraph-legal-map.json")

ALLOWED_REL = {"CONTEXTUAL", "DERIVED", "TEXTUAL"}
ALLOWED_DOMAINS = (
    "https://eur-lex.europa.eu/",
    "https://www.riksdagen.se/",
    "https://svenskforfattningssamling.se/",
    "https://www.echr.coe.int/",
    "https://rm.coe.int/",
)

def fail(msg):
    print("FAIL:", msg)
    raise SystemExit(1)

for p in (ACT, PROVISIONS, PARA_MAP):
    if not p.exists():
        fail(f"missing required file: {p}")

act = ACT.read_text(encoding="utf-8")
preg = json.loads(PROVISIONS.read_text(encoding="utf-8"))
pmap = json.loads(PARA_MAP.read_text(encoding="utf-8"))

provisions = preg.get("provisions", [])
by_id = {}
for item in provisions:
    pid = item.get("id")
    if not pid or pid in by_id:
        fail(f"missing or duplicate provision id: {pid}")
    if item.get("verification_state") != "VERIFIED_PRIMARY_TEXT":
        fail(f"{pid} is not VERIFIED_PRIMARY_TEXT")
    url = item.get("official_url", "")
    if not url.startswith(ALLOWED_DOMAINS):
        fail(f"{pid} uses non-approved official source URL: {url}")
    locator = item.get("locator", "")
    if not locator:
        fail(f"{pid} has empty locator")
    # Exact-locator rule: ranges, vague plurals, and freeform placeholders are forbidden.
    forbidden = ["Arts.", "Articles ", "§§", "–", "—", " to ", "provisions", "where applicable", "incident/recovery"]
    if any(token in locator for token in forbidden):
        fail(f"{pid} locator is not exact enough: {locator}")
    by_id[pid] = item

# Generic citation language is forbidden in the Act.
forbidden_act_patterns = [
    r"\*\*Legal anchors:\*\*",
    r"Arts?\.\s*\d+\s*[–-]\s*\d+",
    r"incident/recovery provisions",
    r"lifecycle risk-management obligations",
    r"governance and compliance architecture",
    r"Cyber Resilience Act\s+—",
    r"DORA,\s+digital operational resilience testing provisions",
]
for pat in forbidden_act_patterns:
    if re.search(pat, act):
        fail(f"generic or ranged citation survived in Act: {pat}")

lines = act.splitlines()
paragraph_markers = {}
visible_refs = {}
section_ids = set(re.findall(r'<!-- cdx:section id="([^"]+)"', act))
section_para_ids = set()

marker_re = re.compile(
    r'^<!-- cdx:legal paragraph="([^"]+)" refs="([^"]+)" verified="(\d{4}-\d{2}-\d{2})" -->$'
)
link_re = re.compile(
    r'\[([^\]]+?) · ([^\]]+?) · (CONTEXTUAL|DERIVED|TEXTUAL)\]\((https://[^)]+)\)'
)

for i, line in enumerate(lines):
    mm = marker_re.match(line)
    if not mm:
        continue
    para_id, refs_field, verified = mm.groups()
    if para_id in paragraph_markers:
        fail(f"duplicate paragraph legal marker: {para_id}")
    refs = []
    for token in refs_field.split(";"):
        if ":" not in token:
            fail(f"{para_id} malformed ref token: {token}")
        pid, rel = token.rsplit(":", 1)
        if rel not in ALLOWED_REL:
            fail(f"{para_id} invalid relationship {rel}")
        if pid not in by_id:
            fail(f"{para_id} references unregistered provision {pid}")
        refs.append((pid, rel))
    if not refs:
        fail(f"{para_id} has no legal references")
    paragraph_markers[para_id] = refs

    # Section-paragraph IDs must encode an existing section ID.
    sec_match = re.match(r'^(CDX-LAW-001-\d{2}-\d{2})-P\d{2}$', para_id)
    if sec_match:
        sec_id = sec_match.group(1)
        if sec_id not in section_ids:
            fail(f"{para_id} encodes non-existent section {sec_id}")
        section_para_ids.add(sec_id)

    # The next line must be the human-visible exact citation block.
    if i + 1 >= len(lines) or not lines[i + 1].startswith("> **Verified legal references:** "):
        fail(f"{para_id} missing immediate visible legal-reference line")
    vr = lines[i + 1]
    links = link_re.findall(vr)
    if len(links) != len(refs):
        fail(f"{para_id} visible link count {len(links)} != marker ref count {len(refs)}")
    for (pid, rel), (label_id, locator, label_rel, url) in zip(refs, links):
        rec = by_id[pid]
        if label_id != pid:
            fail(f"{para_id}: visible id {label_id} != marker id {pid}")
        if locator != rec["locator"]:
            fail(f"{para_id}: locator mismatch for {pid}: {locator} != {rec['locator']}")
        if label_rel != rel:
            fail(f"{para_id}: relationship mismatch for {pid}")
        if url != rec["official_url"]:
            fail(f"{para_id}: URL mismatch for {pid}")
    visible_refs[para_id] = links

missing_sections = sorted(section_ids - section_para_ids)
if missing_sections:
    fail(f"{len(missing_sections)} §§ have no independently cited operative paragraph: {missing_sections[:20]}")

# Map and Act must match exactly at paragraph/ref level.
entries = pmap.get("paragraphs", [])
map_by_id = {}
for item in entries:
    pid = item.get("paragraph_id")
    if not pid or pid in map_by_id:
        fail(f"missing/duplicate paragraph id in paragraph map: {pid}")
    refs = [(x.get("provision_id"), x.get("relationship")) for x in item.get("references", [])]
    map_by_id[pid] = refs

if set(map_by_id) != set(paragraph_markers):
    only_act = sorted(set(paragraph_markers) - set(map_by_id))
    only_map = sorted(set(map_by_id) - set(paragraph_markers))
    fail(f"Act/map paragraph sets differ; only_act={only_act[:10]}, only_map={only_map[:10]}")

for pid, refs in paragraph_markers.items():
    if map_by_id[pid] != refs:
        fail(f"{pid} Act references differ from paragraph map")

# TEXTUAL is a reserved high bar. Current policy requires zero until a separate
# semantic proof record is implemented.
textual = [(pid, rid) for pid, refs in paragraph_markers.items() for rid, rel in refs if rel == "TEXTUAL"]
if textual:
    fail(f"TEXTUAL support used without separate semantic proof records: {textual[:10]}")

print(f"PASS: {len(section_ids)} §§ all have independently cited operative paragraphs")
print(f"PASS: {len(paragraph_markers)} paragraph legal markers are syntactically exact")
print(f"PASS: {len(by_id)} exact provisions are primary-text verified and registered")
print("PASS: Act and paragraph legal map match exactly")
print("PASS: no generic/ranged citation syntax and no unproven TEXTUAL claims")

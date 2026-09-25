#!/usr/bin/env python3
from pathlib import Path
import json,re

def fail(m):
    print("FAIL:",m); raise SystemExit(1)

required=[
 Path("appendices/APP-A-HCC/README.md"),
 Path("appendices/APP-B-EX-INERTA-LIBERTAD/README.md"),
 Path("appendices/APP-C-GLOBAL-AUTHORITY-CORPUS/README.md"),
 Path("GLOBAL-AUTHORITY-CORPUS/authority-registry.json"),
 Path("GLOBAL-AUTHORITY-CORPUS/technical-authorities.json"),
]
for p in required:
    if not p.exists(): fail(f"missing {p}")

hcc=required[0].read_text(encoding="utf-8")
ex=required[1].read_text(encoding="utf-8")
expected="6721ded6009bd771a22d0ed87444386b3a11d69c740d69828e357f1120abce20"
if expected not in hcc: fail("HCC source hash missing")
if expected not in ex: fail("Ex-Inerta source hash missing")
if "HCC-S1-V1.0" not in hcc: fail("HCC source doctrine id missing")
if "CANONICALLY_ADMITTED" not in hcc or "CANONICALLY_ADMITTED" not in ex:
    fail("foundational appendix not canonically admitted")
gac=json.loads(required[3].read_text())
if gac.get("corpus_id")!="CDX-GAC-001" or gac.get("state")!="INSTANTIATED":
    fail("GAC authority registry invalid")
classes=[x["rank"] for x in gac.get("source_classes",[])]
if classes!=["L0","L1","L2","L3","L4","L5","L6","L7","L8"]:
    fail("authority ladder incomplete or reordered")
print("PASS: HCC and Ex-Inerta are canonically admitted with source provenance")
print("PASS: Global Authority Corpus is instantiated with L0-L8 authority classes")

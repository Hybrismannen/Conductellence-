#!/usr/bin/env python3
"""Conductellence automated law integrity audit.

Audit ID: AUD-CDX-LAW-INTEGRITY-001
Law authority:
- 16 kap. 3 § — Auditability state
- 19 kap. 2 § — Versioning
- 19 kap. 6 § — Anti-bloat rule
- 19 kap. 7 § — Exhaustiveness by coverage, not word count
"""

from pathlib import Path
import re
import sys

LAW = Path("LAW/CONDUCTELLENCE-ACT.md")
VALID_AUDITABILITY = {
    "FULLY_AUTOMATABLE",
    "PARTIALLY_AUTOMATABLE",
    "EVIDENCE_AUTOMATABLE",
    "HUMAN_REVIEW_REQUIRED",
    "LEGAL_REVIEW_REQUIRED",
    "CONSTITUTIONAL_HUMAN_ONLY",
}

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)

if not LAW.exists():
    fail("canonical law file missing")

lines = LAW.read_text(encoding="utf-8").splitlines()

if "**Canonical law:** `CDX-LAW-001`" not in "\n".join(lines[:30]):
    fail("canonical law identifier missing from law header")

principles = [line for line in lines if line.startswith("## Principle ")]
if len(principles) != 7:
    fail(f"expected 7 foundational principles, found {len(principles)}")

chapter = None
pending = None
sections = []

chapter_re = re.compile(r"^##\s+(\d+)\s+kap\.")
marker_re = re.compile(
    r'^<!-- cdx:section id="([^"]+)" auditability="([^"]+)" -->$'
)
section_re = re.compile(r"^###\s+(\d+)\s+§\s+(.+)$")

for line_no, line in enumerate(lines, start=1):
    cm = chapter_re.match(line)
    if cm:
        chapter = int(cm.group(1))
        continue

    mm = marker_re.match(line)
    if mm:
        if pending is not None:
            fail(f"unresolved section marker before line {line_no}")
        if chapter is None:
            fail(f"section marker outside chapter at line {line_no}")
        pending = (line_no, chapter, mm.group(1), mm.group(2))
        continue

    sm = section_re.match(line)
    if sm and pending is not None:
        marker_line, ch, sid, auditability = pending
        sec = int(sm.group(1))
        expected_suffix = f"-{ch:02d}-{sec:02d}"
        if not sid.endswith(expected_suffix):
            fail(
                f"{sid} does not match its citation {ch} kap. {sec} § "
                f"(marker line {marker_line})"
            )
        if auditability not in VALID_AUDITABILITY:
            fail(f"{sid} has invalid auditability {auditability}")
        sections.append((sid, auditability, ch, sec, sm.group(2).strip()))
        pending = None

if pending is not None:
    fail(f"final section marker at line {pending[0]} has no section heading")

ids = [s[0] for s in sections]
if len(ids) != len(set(ids)):
    fail("duplicate machine section IDs detected")

if not sections:
    fail("no machine-readable sections detected")

chapters = sorted({s[2] for s in sections})
if chapters != list(range(1, 20)):
    fail(f"expected chapters 1-19, found {chapters}")

print(f"PASS: {len(sections)} §§, 19 chapters, 7 foundational principles")
print("PASS: every § has unique ID and valid auditability class")

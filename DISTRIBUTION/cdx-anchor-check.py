#!/usr/bin/env python3
"""Reference validator for the canonical .cdx/anchor.json estate hook.

The verifier is intentionally network-independent. A governance binding must remain
verifiable from pinned identifiers even when CDX or GitHub is temporarily unavailable.
Live release/drift checks belong in a separate monitoring workflow.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

ANCHOR = Path(".cdx/anchor.json")
EXPECTED_AUTHORITY = "Hybrismannen/Conductellence-"
EXPECTED_NAME = "Conductellence"
EXPECTED_SHORT = "CDX"
EXPECTED_LAW = "CDX-LAW-001"
VALID_BINDING_MODES = {"PINNED_RELEASE", "PINNED_COMMIT", "TRACKING"}
VALID_STATES = {
    "UNBOUND",
    "ANCHOR_DECLARED",
    "CDX_BOUND",
    "CDX_CI_MONITORED",
    "CDX_RUNTIME_GUARDED",
    "CDX_RUNTIME_VERIFIED",
    "CDX_DEGRADED",
    "CDX_REVOKED",
}
RUNTIME_STATES = {"CDX_RUNTIME_GUARDED", "CDX_RUNTIME_VERIFIED"}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    require(ANCHOR.exists(), ".cdx/anchor.json missing")
    try:
        doc = json.loads(ANCHOR.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"anchor is not valid JSON: {exc}")

    require(doc.get("schema") == "cdx.anchor/v1", "unsupported anchor schema")
    require(doc.get("system_short_name") == EXPECTED_SHORT, "system_short_name must be CDX")
    require(doc.get("law_id") == EXPECTED_LAW, f"law_id must be {EXPECTED_LAW}")

    authority = doc.get("cdx_authority") or {}
    require(authority.get("repository") == EXPECTED_AUTHORITY, "unknown CDX authority repository")
    require(authority.get("canonical_name") == EXPECTED_NAME, "canonical authority name mismatch")
    require(authority.get("short_name") in (None, EXPECTED_SHORT), "authority short_name mismatch")

    governed = doc.get("governed_surface") or {}
    require(bool(governed.get("identity")), "governed_surface.identity missing")
    github_repo = os.getenv("GITHUB_REPOSITORY")
    if github_repo and governed.get("repository"):
        require(governed["repository"] == github_repo, "anchor repository does not match GITHUB_REPOSITORY")

    mode = doc.get("binding_mode")
    require(mode in VALID_BINDING_MODES, "invalid binding_mode")
    pin = doc.get("policy_pin") or {}
    ref_type = pin.get("ref_type")
    ref = pin.get("ref")
    require(bool(ref_type) and bool(ref), "policy_pin.ref_type and policy_pin.ref are required")

    if mode == "PINNED_COMMIT":
        require(ref_type == "COMMIT", "PINNED_COMMIT requires ref_type COMMIT")
        require(bool(re.fullmatch(r"[0-9a-fA-F]{40}", str(ref))), "PINNED_COMMIT ref must be a 40-character commit SHA")
    elif mode == "PINNED_RELEASE":
        require(ref_type in {"RELEASE", "TAG", "POLICY_DIGEST"}, "PINNED_RELEASE requires RELEASE, TAG or POLICY_DIGEST")

    state = doc.get("binding_state")
    require(state in VALID_STATES, "invalid binding_state")

    enforcement = doc.get("local_enforcement") or {}
    require(bool(enforcement.get("owner")), "local_enforcement.owner missing")
    points = enforcement.get("points")
    require(isinstance(points, list), "local_enforcement.points must be an array")
    if state in RUNTIME_STATES:
        require(len(points) > 0, "runtime-bound state requires at least one local enforcement point")
        require(
            enforcement.get("fail_closed_for_consequential_effects") is True,
            "runtime-bound state requires fail_closed_for_consequential_effects=true",
        )

    auth_ctx = doc.get("authority_context") or {}
    if state in RUNTIME_STATES:
        require(auth_ctx.get("authority_ref_required") is True, "runtime-bound state requires authority_ref")
        require(auth_ctx.get("mandate_ref_required") is True, "runtime-bound state requires mandate_ref")

    verification = doc.get("verification") or {}
    require(bool(verification.get("verification_state")), "verification.verification_state missing")

    if mode == "TRACKING" and state in {"CDX_RUNTIME_GUARDED", "CDX_RUNTIME_VERIFIED"}:
        fail("TRACKING governance targets cannot claim runtime-verified standing")

    print(
        "PASS: CDX anchor "
        f"{governed.get('identity')} -> {EXPECTED_AUTHORITY} "
        f"mode={mode} ref={ref} state={state}"
    )


if __name__ == "__main__":
    main()

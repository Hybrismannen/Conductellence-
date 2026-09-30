# Conductellence RED-TEAM

**Suite ID:** `CDX-RED-001`

This subsystem contains critical adversarial acceptance cases for the Conductellence reference runtime.

The suite is deliberately narrow and constitutional: it tests whether known high-consequence failure patterns remain fail-closed, including self-escalation, delegation overflow, Z0 boundary violation, content-to-authority mutation, missing permission, tool-availability confusion, fail-open evaluation, emergency authority expansion, scenario escape, external-effect bypass, missing SPETL evidence and ignored security stops.

Passing this suite is required for core reference-runtime remediation and for any future transition to `ENFORCING`.

The suite is not a substitute for broader penetration testing, provider-specific red teaming or application-specific adversarial testing.

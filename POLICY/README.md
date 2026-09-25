# Conductellence Policy Plane

This directory implements the deterministic reference policy runtime for `CDX-LAW-001`.

- `control-registry.json` contains the executable control objects.
- `engine.py` evaluates controls by enforcement surface.
- unknown or malformed evaluation fails closed.
- policy decisions do not create identity, authority or mandate.
- production integrations invoke these controls at their own enforcement points and emit SPETL evidence.

The reference runtime is intentionally separate from external systems: Conductellence defines the policy; governed systems enforce it locally or through an approved policy service.

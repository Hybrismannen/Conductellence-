"""Offline contract check for an unadopted CDX Drive control proposal."""
import json
from pathlib import Path
import unittest

from POLICY.engine import eval_rule

PROPOSAL = Path("POLICY/proposals/OAI-DRIVE-EXTERNAL-EFFECT-CONTROL-v1.1.json")


class CandidateDrivePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(PROPOSAL.read_text(encoding="utf-8"))
        cls.rule = cls.manifest["proposed_control"]["predicate"]

    def test_all_claimed_test_vectors(self):
        vectors = self.manifest["proposed_control"]["test_vectors"]
        self.assertGreaterEqual(len(vectors), 10)
        for vector in vectors:
            with self.subTest(name=vector["name"]):
                ok = eval_rule(self.rule, vector["context"])
                expected = vector["expected"] == "ALLOW"
                self.assertEqual(ok, expected)

    def test_missing_drive_context_denies(self):
        self.assertFalse(eval_rule(self.rule,
                                   {"surface":"EXTERNAL_EFFECT",
                                    "provider_id":"google_drive"}))

    def test_unknown_operations_deny(self):
        sample = self.manifest["proposed_control"]["test_vectors"][0]["context"]
        for operation in ("DELETE", "COPY", "UPDATE", "UNKNOWN", None):
            with self.subTest(operation=operation):
                context = json.loads(json.dumps(sample))
                context["drive_guard"]["operation"] = operation
                self.assertFalse(eval_rule(self.rule, context))

    def test_not_active_registered_control(self):
        registry = json.loads(Path("POLICY/control-registry.json").read_text(encoding="utf-8"))
        ids = {entry["control_id"] for entry in registry["controls"]}
        self.assertNotIn(self.manifest["proposed_control"]["control_id"], ids)
        self.assertEqual(self.manifest["status"], "CANDIDATE_NOT_ACTIVE")


if __name__ == "__main__":
    unittest.main()

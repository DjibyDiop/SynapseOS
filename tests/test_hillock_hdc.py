"""
Unit & Integration Tests for Hillock Neuro-Symbolic HDC Memory Engine (`cortex/hillock_hdc.py`)
================================================================================================
Verifies:
  1. Hyperdimensional Computing (HDC / VSA) bitwise algebra (XOR binding, permutation, POPCNT similarity).
  2. One-Shot Hebbian Learning (<0.1ms fact binding without retraining).
  3. Anti-Hallucination Guardrail (Fact Verification & Refutation).
  4. Integration with CortexEngine.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cortex.hillock_hdc import Hypervector, HillockHDCStore, get_hillock_store
from cortex.engine import CortexEngine


class TestHillockHDC(unittest.TestCase):
    def setUp(self):
        self.store = get_hillock_store()
        self.engine = CortexEngine()

    def test_hypervector_determinism_and_orthogonality(self):
        h1 = Hypervector.from_symbol("Moon")
        h2 = Hypervector.from_symbol("Moon")
        h3 = Hypervector.from_symbol("Mars")

        # Deterministic
        self.assertEqual(h1.val, h2.val)
        self.assertEqual(h1.similarity(h2), 1.0)

        # Quasi-orthogonal for different symbols (~ 0.0)
        sim = h1.similarity(h3)
        self.assertAlmostEqual(sim, 0.0, delta=0.08)

    def test_hypervector_binding_is_self_inverse(self):
        h_a = Hypervector.from_symbol("Rocket")
        h_b = Hypervector.from_symbol("Thruster")
        bound = h_a.bind(h_b)

        # Unbinding: (A ⊗ B) ⊗ B = A
        unbound = bound.bind(h_b)
        self.assertEqual(unbound.val, h_a.val)
        self.assertEqual(unbound.similarity(h_a), 1.0)

    def test_hypervector_permutation(self):
        h = Hypervector.from_symbol("Sensor")
        p1 = h.permute(3)
        inv_p = p1.inv_permute(3)
        self.assertEqual(inv_p.val, h.val)
        self.assertNotEqual(p1.val, h.val)

    def test_one_shot_hebbian_learning(self):
        success = self.store.teach_fact("SatelliteAlpha", "orbital_altitude_km", "450", source="test_lab")
        self.assertTrue(success)

        res = self.store.verify_fact("SatelliteAlpha", "orbital_altitude_km", "450")
        self.assertTrue(res["verified"])
        self.assertEqual(res["ground_truth_object"], "450")
        self.assertIn("Verified Fact", res["explanation"])

    def test_anti_hallucination_refutation(self):
        # Claim that Moon gravity is 9.8 (Earth gravity)
        res = self.store.verify_fact("Moon", "gravity_m_s2", "9.80")
        self.assertFalse(res["verified"])
        self.assertEqual(res["ground_truth_object"], "1.62")
        self.assertIn("Factual Refutation", res["explanation"])

    def test_unverified_relation_refusal(self):
        # An unknown relation should be cleanly refused without hallucinating
        res = self.store.verify_fact("Moon", "favorite_ice_cream_flavor", "vanilla")
        self.assertFalse(res["verified"])
        self.assertIsNone(res["ground_truth_object"])
        self.assertIn("Anti-Hallucination Guardrail", res["explanation"])

    def test_cortex_engine_hillock_integration(self):
        ans = self.engine.explain_ai_concept("?verify Moon gravity is 1.62")
        self.assertIn("Hillock", ans["source"])
        self.assertIn("Verified Fact", ans["summary"])


if __name__ == "__main__":
    unittest.main()

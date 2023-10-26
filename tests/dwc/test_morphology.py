import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "morphology"


class TestMorphology(unittest.TestCase):
    def test_morphology_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "homomorphic")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"morphology": "homomorphic"}})

import unittest

from tests.setup import to_ent

LABEL = "morphology"


class TestMorphology(unittest.TestCase):
    def test_morphology_dwc_01(self):
        ent = to_ent(LABEL, "homomorphic")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dynamicProperties": {"morphology": "homomorphic"}}
        )

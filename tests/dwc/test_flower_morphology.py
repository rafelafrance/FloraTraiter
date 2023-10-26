import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "flower_morphology"


class TestFlowerMorphology(unittest.TestCase):
    def test_flower_morphology_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "accrescent")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual, {"dynamicProperties": {"flowerMorphology": "accrescent"}}
        )

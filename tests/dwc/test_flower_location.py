import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "flower_location"


class TestFlowerLocation(unittest.TestCase):
    def test_flower_location_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "epigynous")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"flowerLocation": "inferior"}})

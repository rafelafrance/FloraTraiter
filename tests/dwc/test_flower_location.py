import unittest

from tests.setup import to_ent

LABEL = "flower_location"


class TestFlowerLocation(unittest.TestCase):
    def test_flower_location_dwc_01(self):
        ent = to_ent(LABEL, "epigynous")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"flowerLocation": "inferior"}}
        )

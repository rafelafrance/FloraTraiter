import unittest

from tests.setup import to_ent

LABEL = "woodiness"


class TestWoodiness(unittest.TestCase):
    def test_venation_01(self):
        ent = to_ent(LABEL, "Herbs perennial or subshrubs")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"shrubWoodiness": "herb"}}
        )

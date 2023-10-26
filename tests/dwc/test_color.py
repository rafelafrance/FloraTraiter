import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "color"


class TestColor(unittest.TestCase):
    def test_color_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "male leaf margin green")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual, {"dynamicProperties": {"maleLeafMarginColor": "green"}}
        )

    def test_color_dwc_02(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "flower petals not purple-spotted")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual, {"dynamicProperties": {"missingFlowerPetalColor": "purple-spotted"}}
        )

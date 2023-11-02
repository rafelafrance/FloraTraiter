import unittest

from tests.setup import to_dwc

LABEL = "color"


class TestColor(unittest.TestCase):
    def test_color_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "male leaf margin green"),
            {"dwc:dynamicProperties": {"maleLeafMarginColor": "green"}},
        )

    def test_color_dwc_02(self):
        self.assertEqual(
            to_dwc(LABEL, "flower petals not purple-spotted"),
            {"dwc:dynamicProperties": {"missingFlowerPetalColor": "purple-spotted"}},
        )

import unittest

from tests.setup import to_dwc

LABEL = "color"


class TestColor(unittest.TestCase):
    def test_color_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "green"),
            {"dwc:dynamicProperties": {"color": "green"}},
        )

    def test_color_dwc_02(self):
        self.assertEqual(
            to_dwc(LABEL, "not purple-spotted"),
            {"dwc:dynamicProperties": {"missingColor": "purple-spotted"}},
        )

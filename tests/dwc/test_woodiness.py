import unittest

from tests.setup import to_dwc

LABEL = "woodiness"


class TestWoodiness(unittest.TestCase):
    def test_venation_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Herbs perennial or subshrubs"),
            {"dwc:dynamicProperties": {"shrubWoodiness": "herb"}},
        )

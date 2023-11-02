import unittest

from tests.setup import to_dwc

LABEL = "flower_location"


class TestFlowerLocation(unittest.TestCase):
    def test_flower_location_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "epigynous"),
            {"dwc:dynamicProperties": {"flowerLocation": "inferior"}},
        )

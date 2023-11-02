import unittest

from tests.setup import to_dwc

LABEL = "flower_morphology"


class TestFlowerMorphology(unittest.TestCase):
    def test_flower_morphology_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "accrescent"),
            {"dwc:dynamicProperties": {"flowerMorphology": "accrescent"}},
        )

import unittest

from tests.setup import to_dwc

LABEL = "morphology"


class TestMorphology(unittest.TestCase):
    def test_morphology_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "homomorphic"),
            {"dwc:dynamicProperties": {"morphology": "homomorphic"}},
        )

import unittest

from tests.setup import to_dwc

LABEL = "venation"


class TestVenation(unittest.TestCase):
    def test_venation_01(self):
        self.assertEqual(
            to_dwc(LABEL, "leaf subflabellate"),
            {"dwc:dynamicProperties": {"leafVenation": "subflabellate"}},
        )

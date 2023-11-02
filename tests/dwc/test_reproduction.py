import unittest

from tests.setup import to_dwc

LABEL = "reproduction"


class TestReproduction(unittest.TestCase):
    def test_reproduction_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "gynodioecious"),
            {"dwc:dynamicProperties": {"reproduction": "gynodioecious"}},
        )

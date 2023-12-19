import unittest

from tests.setup import to_dwc

LABEL = "habitat"


class TestHabitat(unittest.TestCase):
    def test_habitat_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "subalpine zone"), {"dwc:habitat": "subalpine zone"}
        )
